#!/usr/bin/env python3
"""Card quadrado 1080x1080 "Quanto o seu sistema vai gerar por mês?" (para WhatsApp do cliente).

Uso: python3 card_geracao.py clientes/<cliente>.json "Card Geracao - Nome - DD-MM-AAAA.png"
Lê do JSON do orçamento: cliente, cidade, placas_qtd, placa_w, data, validade_dias.
As contas saem do código (117 kWh por kWp ao mês, método oficial da Insolar).
"""
import json, subprocess, sys, tempfile, os, datetime as dt

FATOR = 117  # kWh por kWp por mês (região de Ilhéus)
AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def milhar(x):
    return f"{x:,.0f}".replace(",", ".")


def virgula(x, casas=2):
    return f"{x:.{casas}f}".replace(".", ",")


def main(json_path, saida):
    d = json.load(open(json_path, encoding="utf-8"))
    n, w = d["placas_qtd"], d["placa_w"]
    kwp = n * w / 1000
    mes = kwp * FATOR
    dia = mes / 30
    ano = mes * 12
    validade = dt.date.fromisoformat(d["data"]) + dt.timedelta(days=d["validade_dias"])
    cidade = d["cidade"].replace(" - BA", "")
    partes = [p.strip() for p in cidade.split(",")]
    cidade_txt = ", ".join(reversed(partes)) if len(partes) == 2 else cidade
    robo = os.path.join(RAIZ, "robo-oficial", "precos", "robo_tablet_placas_dia.png")
    logo = os.path.join(AQUI, "img", "S_grande.png")

    print(f"CONTA: {n} x {w} W = {kwp:.2f} kWp | x {FATOR} = {mes:.1f} kWh/mês | dia {dia:.1f} | ano {ano:.0f}")

    html = f"""<!doctype html><html><head><meta charset="utf-8"><style>
*{{box-sizing:border-box;margin:0;padding:0}}
html,body{{width:1080px;height:1080px;overflow:hidden;font-family:'Inter',sans-serif;color:#fff;background:#0A1F47}}
.bg{{position:absolute;inset:0;background:radial-gradient(900px 700px at 20% 15%,#16409A 0%,#0E2A5E 45%,#07173A 100%)}}
.robo{{position:absolute;right:0;top:0;height:1080px;width:607px;object-fit:cover;
  -webkit-mask-image:linear-gradient(to right,transparent 0,#000 38%);mask-image:linear-gradient(to right,transparent 0,#000 38%)}}
.fundo{{position:absolute;left:0;right:0;bottom:0;height:300px;background:linear-gradient(to top,rgba(5,14,38,.92),rgba(5,14,38,0))}}
.col{{position:absolute;left:56px;top:0;width:690px;height:1080px}}
.tag{{position:absolute;top:48px;left:0;font-family:'Inter Display';font-weight:800;font-size:20px;letter-spacing:.14em;color:#F9B91E;
  border:2px solid #F9B91E;border-radius:40px;padding:9px 22px;background:rgba(249,185,30,.1)}}
h1{{position:absolute;top:118px;left:0;width:690px;font-family:'Inter Display';font-weight:800;font-size:58px;line-height:1.06;letter-spacing:-.01em}}
h1 span{{color:#F9B91E}}
.numero{{position:absolute;top:262px;left:0;width:640px;height:210px;border-radius:28px;background:rgba(255,255,255,.08);
  border:1.5px solid rgba(160,200,255,.28);padding:14px 30px;backdrop-filter:blur(4px)}}
.numero .v{{font-family:'Inter Display';font-weight:800;font-size:150px;line-height:1;color:#F9B91E;letter-spacing:-.03em;display:flex;align-items:baseline;gap:16px}}
.numero .v small{{font-size:56px;color:#fff;letter-spacing:0}}
.numero .l{{font-size:30px;font-weight:600;color:#DCE6FA;margin-top:2px}}
.conta{{position:absolute;top:492px;left:0;width:640px;border-radius:24px;background:rgba(61,255,143,.09);border:1.5px solid rgba(61,255,143,.45);padding:18px 26px}}
.conta .t{{font-size:17px;letter-spacing:.16em;font-weight:700;color:#3DFF8F;margin-bottom:8px}}
.conta .r{{font-family:'Inter Display';font-weight:700;font-size:30px;line-height:1.35}}
.conta .r b{{color:#F9B91E}}
.conta .s{{font-size:18px;color:#B9C8E6;margin-top:6px;line-height:1.3}}
.chips{{position:absolute;top:690px;left:0;display:flex;gap:16px}}
.chip{{border-radius:18px;background:rgba(255,255,255,.1);border:1.5px solid rgba(160,200,255,.3);padding:12px 22px}}
.chip b{{font-family:'Inter Display';font-size:32px;color:#fff;font-weight:800;display:block}}
.chip i{{font-style:normal;font-size:18px;color:#C9D5EC}}
.simples{{position:absolute;top:790px;left:0;width:640px;font-size:25px;line-height:1.3;color:#EAF0FC}}
.simples b{{color:#F9B91E}}
.botao{{position:absolute;top:894px;left:0;background:#F9B91E;color:#0E2A5E;font-family:'Inter Display';font-weight:800;font-size:30px;
  border-radius:50px;padding:14px 34px;display:flex;align-items:center;gap:12px}}
.miuda{{position:absolute;top:970px;left:0;width:680px;font-size:14.5px;line-height:1.32;color:#AFC0DE}}
.logo{{position:absolute;right:46px;bottom:150px;height:96px;filter:drop-shadow(0 4px 14px rgba(0,0,0,.5))}}
.marca{{position:absolute;right:42px;bottom:118px;width:130px;text-align:center;font-family:'Inter Display';font-weight:800;font-size:15px;letter-spacing:.12em;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.7)}}
.cli{{position:absolute;right:42px;top:48px;font-size:17px;font-weight:600;color:#fff;text-shadow:0 2px 8px rgba(0,0,0,.8);text-align:right;line-height:1.3}}
</style></head><body>
<div class="bg"></div>
<img class="robo" src="file://{robo}">
<div class="fundo"></div>
<div class="cli">Proposta do {d['cliente']}<br>{cidade_txt}</div>
<img class="logo" src="file://{logo}">
<div class="marca">INSOLAR<br>BRASIL</div>
<div class="col">
  <div class="tag">SUA GERAÇÃO DE ENERGIA</div>
  <h1>Quanto o seu sistema vai <span>gerar por mês?</span></h1>
  <div class="numero"><div class="v">≈ {milhar(mes)} <small>kWh</small></div><div class="l">de energia por mês, em média</div></div>
  <div class="conta">
    <div class="t">COMO CHEGAMOS NESSE NÚMERO</div>
    <div class="r">{n} placas × {w} W = <b>{virgula(kwp)} kWp</b></div>
    <div class="r">{virgula(kwp)} kWp × {FATOR} = <b>{milhar(mes)} kWh/mês</b></div>
    <div class="s">Cada 1 kWp gera, em média, {FATOR} kWh por mês na região.</div>
  </div>
  <div class="chips">
    <div class="chip"><b>≈ {milhar(dia)} kWh</b><i>por dia</i></div>
    <div class="chip"><b>≈ {milhar(round(ano, -2))} kWh</b><i>por ano</i></div>
  </div>
  <div class="simples">Em palavras simples: <b>são as placas do seu telhado produzindo energia</b> para a sua casa todos os meses.</div>
  <div class="botao">Fale com a Insolar: (73) 3223-5102</div>
  <div class="miuda">*Estimativa: {virgula(kwp)} kWp × {FATOR} kWh = {milhar(mes)} kWh por mês. A geração real varia com o clima, sombra, inclinação e direção do telhado. Valores de referência, sujeitos a análise técnica. Condição válida até {validade.strftime('%d/%m/%Y')}.</div>
</div>
</body></html>"""

    tmp = tempfile.mkdtemp()
    arq = os.path.join(tmp, "card.html")
    open(arq, "w", encoding="utf-8").write(html)
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu", "--hide-scrollbars",
                    "--allow-file-access-from-files", "--force-device-scale-factor=1",
                    "--window-size=1080,1080", f"--screenshot={saida}", f"file://{arq}"],
                   check=True, capture_output=True)
    print("OK", saida, os.path.getsize(saida), "bytes")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
