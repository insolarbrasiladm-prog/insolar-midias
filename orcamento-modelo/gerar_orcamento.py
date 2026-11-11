#!/usr/bin/env python3
"""Gerador do orçamento Insolar Brasil (modelo tecnológico com o robô oficial).
Uso: python3 gerar_orcamento.py dados.json saida.pdf
Todas as contas são feitas aqui, em código. Nada de cabeça."""
import json, sys, subprocess, os, math, datetime
from jinja2 import Template

AQUI = os.path.dirname(os.path.abspath(__file__))
GERACAO_KWH_POR_KWP = 120  # decisão do Cristiano em 08/11/2026 (igual à planilha de preços; rever em dezembro)
DESGASTE_ANO = 0.005

def brl(v):
    s = f"{v:,.2f}"
    return "R$ " + s.replace(",", "X").replace(".", ",").replace("X", ".")

def num(v, casas=0):
    s = f"{v:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")

def parcela(valor, taxa, n):
    return valor * taxa / (1 - (1 + taxa) ** -n)

def calcular(d):
    c = {}
    kwp = d["placas_qtd"] * d["placa_w"] / 1000
    c["kwp"] = kwp
    c["fator"] = GERACAO_KWH_POR_KWP
    c["geracao_mes"] = kwp * GERACAO_KWH_POR_KWP
    c["geracao_ano"] = c["geracao_mes"] * 12
    anos = [c["geracao_ano"] * (1 - DESGASTE_ANO) ** a for a in range(25)]
    c["geracao_25"] = sum(anos)
    acum, s = [], 0
    for g in anos:
        s += g; acum.append(s)
    c["acum"] = acum
    c["inversor_ok"] = d["inversor_kw"] * 1.0 >= kwp / 1.3  # inversor aceita até ~30% a mais de placas
    p = d["preco"]
    c["pix"] = p * (1 - d.get("desconto_pix", 0.05))
    c["cartao12"] = p / 12
    fin = []
    if p >= 10000:
        for n, taxa in d["financiamento"]:
            fin.append((n, taxa, parcela(p, taxa, n)))
    c["fin"] = fin
    if d.get("bateria"):
        c["opcoes"] = []
        for o in d["bateria"]["opcoes"]:
            o2 = dict(o)
            o2["fin"] = [(n, taxa, parcela(o["preco"], taxa, n)) for n, taxa in d["financiamento"]]
            c["opcoes"].append(o2)
    return c

def grafico_svg(acum):
    w, h, pad = 520, 190, 34
    mx = acum[-1]
    bw = (w - pad - 10) / len(acum)
    out = [f'<svg viewBox="0 0 {w} {h+28}" xmlns="http://www.w3.org/2000/svg">']
    out.append('<defs><linearGradient id="gb" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="#16c784"/><stop offset="1" stop-color="#7CFFB2"/></linearGradient></defs>')
    for i in range(5):
        y = 10 + (h - 10) * i / 4
        val = mx * (1 - i / 4)
        out.append(f'<line x1="{pad}" x2="{w}" y1="{y:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,.08)"/>')
        out.append(f'<text x="{pad-4}" y="{y+3:.1f}" fill="#8FA3C7" font-size="8" text-anchor="end">{num(val/1000)} mil</text>')
    for i, v in enumerate(acum):
        bh = (h - 10) * v / mx
        x = pad + i * bw + 2
        out.append(f'<rect x="{x:.1f}" y="{h-bh:.1f}" width="{bw-4:.1f}" height="{bh:.1f}" rx="2" fill="url(#gb)" opacity="{0.55+0.45*i/24:.2f}"/>')
        if i in (0, 4, 9, 14, 19, 24):
            out.append(f'<text x="{x+(bw-4)/2:.1f}" y="{h+14}" fill="#8FA3C7" font-size="8" text-anchor="middle">ano {i+1}</text>')
    out.append('</svg>')
    return "".join(out)

def gerar(dados_path, saida):
    d = json.load(open(dados_path, encoding="utf-8"))
    c = calcular(d)
    hoje = datetime.date.fromisoformat(d["data"])
    html = Template(open(os.path.join(AQUI, "modelo.html"), encoding="utf-8").read()).render(
        d=d, c=c, brl=brl, num=num, grafico=grafico_svg(c["acum"]),
        data_br=hoje.strftime("%d/%m/%Y"),
        validade_br=(hoje + datetime.timedelta(days=d.get("validade_dias", 3))).strftime("%d/%m/%Y"),
        img="file://" + os.path.join(AQUI, "img"))
    tmp = os.path.join(AQUI, "_orcamento.html")
    open(tmp, "w", encoding="utf-8").write(html)
    subprocess.run(["google-chrome", "--headless=new", "--no-sandbox", "--disable-gpu",
                    "--allow-file-access-from-files", "--no-pdf-header-footer",
                    f"--print-to-pdf={os.path.abspath(saida)}", "file://" + tmp],
                   check=True, capture_output=True)
    return c

def capa_whatsapp(pdf):
    """Imagem QUADRADA 1080x1080 da capa, para mandar no WhatsApp antes do PDF
    (regra: foto com texto no WhatsApp = quadrada, nada cortado)."""
    from PIL import Image
    base = os.path.splitext(os.path.abspath(pdf))[0]
    subprocess.run(["pdftoppm", "-r", "200", "-png", "-f", "1", "-l", "1", "-singlefile", pdf, base + "_capa"], check=True, capture_output=True)
    im = Image.open(base + "_capa.png").convert("RGB")
    S = 1080; h = S - 40; w = int(im.width * h / im.height)
    out = Image.new("RGB", (S, S), im.getpixel((10, 10)))
    out.paste(im.resize((w, h), Image.LANCZOS), ((S - w) // 2, 20))
    dest = os.path.join(os.path.dirname(base), "Capa WhatsApp - " + os.path.basename(base) + ".jpg")
    out.save(dest, quality=90); os.remove(base + "_capa.png")
    return dest

if __name__ == "__main__":
    c = gerar(sys.argv[1], sys.argv[2])
    print("Capa para WhatsApp:", capa_whatsapp(sys.argv[2]))
    print(json.dumps({k: v for k, v in c.items() if k != "acum"}, ensure_ascii=False, indent=1, default=str))
