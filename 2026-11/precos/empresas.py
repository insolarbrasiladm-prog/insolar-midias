import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
R='/home/claude/insolar-midias/robo-oficial/precos/'
FD='/usr/share/fonts/opentype/inter/'
def F(n,s): return ImageFont.truetype(FD+n,s)
W,H=1080,1350
BG=(4,14,34); WHITE=(255,255,255); SOFT=(200,212,235); GOLD=(255,184,28); ORANGE=(255,122,26); GREEN=(57,230,110)
LOGO=Image.open('logo.png').convert('RGBA')
VAL='01/11 a 03/11/2026'
os.makedirs('out/empresas',exist_ok=True)

def brl(v,cent=True):
    s=f'{v:,.2f}' if cent else f'{v:,.0f}'
    return s.replace(',','X').replace('.',',').replace('X','.')

def base(img,x0=None):
    c=Image.new('RGB',(W,H),BG)
    im=Image.open(R+img).convert('RGB'); s=H/im.height
    im=im.resize((int(im.width*s),H),Image.LANCZOS)
    x=W-im.width if x0 is None else x0
    c.paste(im,(x,0))
    # degradê suave na emenda esquerda
    g=Image.new('L',(W,H),0); d=ImageDraw.Draw(g)
    for i in range(160):
        d.line([(x+i,0),(x+i,H)],fill=int(255*(1-i/160)))
    d.rectangle([0,0,x,H],fill=255)
    c.paste(Image.new('RGB',(W,H),BG),(0,0),g)
    return c

SIMB=Image.open('simbolo.png').convert('RGBA')
def logo(c,x=56,y=56,w=None):
    h=86; l=SIMB.resize((int(SIMB.width*h/SIMB.height),h),Image.LANCZOS); c.paste(l,(x,y),l)
    d=ImageDraw.Draw(c); tx=x+l.width+18
    d.text((tx,y+4),'INSOLAR',font=F('InterDisplay-Black.otf',44),fill=WHITE)
    d.text((tx,y+52),'BRASIL · ENERGIA SOLAR',font=F('Inter-Bold.otf',20),fill=GOLD)

def wrap(d,txt,f,maxw):
    out=[];line=''
    for w in txt.split():
        t=(line+' '+w).strip()
        if d.textlength(t,font=f)<=maxw: line=t
        else: out.append(line); line=w
    out.append(line); return out

def rodape(c,legal):
    ov=Image.new('RGBA',(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
    od.rectangle([0,1118,W,H],fill=(2,8,22,235)); c.paste(ov,(0,0),ov)
    d=ImageDraw.Draw(c); f=F('Inter-Regular.otf',19); y=1134
    for ln in wrap(d,legal,f,W-100):
        d.text((50,y),ln,font=f,fill=SOFT); y+=25
    d.text((50,H-48),'WhatsApp (73) 3223-5102',font=F('Inter-Bold.otf',28),fill=GOLD)
    d.text((W-50,H-46),'Insolar Brasil',font=F('Inter-SemiBold.otf',24),fill=WHITE,anchor='ra')

def tag(d,x,y,txt):
    f=F('Inter-Black.otf',26); w=d.textlength(txt,font=f)
    d.rounded_rectangle([x,y,x+w+36,y+48],radius=24,fill=ORANGE)
    d.text((x+18,y+9),txt,font=f,fill=WHITE)

def card(n,k):
    c=base('robo_apontando_placas.png'); logo(c); d=ImageDraw.Draw(c); X=56
    tag(d,X,190,'BLACK NOVEMBRO')
    d.text((X,268),'Consumo de até',font=F('Inter-Medium.otf',32),fill=SOFT)
    fb=F('InterDisplay-Black.otf',100); d.text((X,300),f"{k['kwh']:,}".replace(',','.'),font=fb,fill=WHITE)
    wv=d.textlength(f"{k['kwh']:,}".replace(',','.'),font=fb)
    d.text((X+wv+10,355),'kWh',font=F('Inter-Bold.otf',38),fill=WHITE)
    d.text((X,420),f"{k['placas']} placas de 620 W · {k['kwp']} kWp",font=F('Inter-Medium.otf',26),fill=SOFT)
    y=480
    if k.get('p120'):
        d.text((X,y),'parcelas a partir de',font=F('Inter-Medium.otf',30),fill=SOFT)
        inteiro,cent=brl(k['p120']).split(','); fp=F('InterDisplay-Black.otf',112 if len(inteiro)<=3 else 84)
        t='R$ '+inteiro; d.text((X-4,y+30),t,font=fp,fill=GOLD); wv=d.textlength(t,font=fp)
        d.text((X+wv+4,y+52),','+cent,font=F('Inter-Black.otf',44),fill=GOLD)
        d.text((X+wv+4,y+104),'/mês',font=F('Inter-Bold.otf',30),fill=GOLD)
        d.text((X,y+165),'em 120x',font=F('Inter-Black.otf',40),fill=WHITE)
        f=F('Inter-SemiBold.otf',30)
        d.text((X,y+228),f"84x de R$ {brl(k['p84'])}",font=f,fill=WHITE)
        d.text((X,y+268),f"60x de R$ {brl(k['p60'])}",font=f,fill=WHITE)
        y+=320
        d.text((X,y),'12x SEM JUROS no cartão',font=F('Inter-Black.otf',27),fill=GREEN)
        d.text((X,y+34),f"de R$ {brl(k['p12'])}",font=F('Inter-Bold.otf',30),fill=WHITE)
        y+=96
    else:
        d.text((X,y),'12x SEM JUROS no cartão',font=F('Inter-Black.otf',30),fill=GREEN)
        fp=F('InterDisplay-Black.otf',112); inteiro,cent=brl(k['p12']).split(',')
        t='R$ '+inteiro; d.text((X-4,y+36),t,font=fp,fill=GOLD); wv=d.textlength(t,font=fp)
        d.text((X+wv+4,y+58),','+cent,font=F('Inter-Black.otf',44),fill=GOLD)
        d.text((X+wv+4,y+110),'/mês',font=F('Inter-Bold.otf',30),fill=GOLD)
        d.text((X,y+175),'Kit de entrada:',font=F('Inter-SemiBold.otf',28),fill=SOFT)
        d.text((X,y+210),'pagamento no cartão ou Pix',font=F('Inter-SemiBold.otf',28),fill=SOFT)
        y+=330
    # caixa Pix
    d.rounded_rectangle([X,y,X+430,y+112],radius=18,fill=(255,255,255))
    d.text((X+22,y+12),'À VISTA NO PIX',font=F('Inter-Black.otf',24),fill=(11,31,68))
    d.text((X+22,y+42),f"R$ {brl(k['pix'],False)}",font=F('InterDisplay-Black.otf',56),fill=ORANGE)
    legal=(f"*Oferta válida de {VAL}. Preço por sistema individual, para uma unidade consumidora, sujeito a análise técnica. "
           f"Preço a prazo: R$ {brl(k['tab'],False)}. ")
    if k.get('p120'):
        legal+=(f"Parcelas sujeitas à aprovação de crédito, aos critérios de cada financeira, ao score e à capacidade de pagamento de cada CPF/CNPJ. "
                f"Taxa de referência: 1,39% ao mês (24x a 84x) e 1,55% ao mês (120x); total em 120x: R$ {brl(k['p120']*120)}. ")
    legal+=f"12x sem juros no cartão conforme limite disponível. Geração estimada de {k['kwh']:,} kWh por mês, varia com o local e a sombra.".replace(f"{k['kwh']:,}",f"{k['kwh']:,}".replace(',','.'))
    rodape(c,legal)
    c.save(f'out/empresas/{n:02d}_kit_{k["kwh"]}.jpg',quality=92)

def capa():
    c=base('robo_tablet_parcelas.png',x0=(W-759)//2+180); logo(c,w=230); d=ImageDraw.Draw(c); X=56
    tag(d,X,230,'BLACK NOVEMBRO')
    f=F('InterDisplay-Black.otf',84)
    for i,t in enumerate(['TABELA','EMPRESAS','E AGRO']): d.text((X,310+i*92),t,font=f,fill=WHITE if i<2 else GOLD)
    d.text((X,600),'Usinas a partir de',font=F('Inter-SemiBold.otf',30),fill=SOFT)
    fp=F('InterDisplay-Black.otf',104); t='R$ 935'; d.text((X-4,632),t,font=fp,fill=GOLD); wv=d.textlength(t,font=fp)
    d.text((X+wv+4,652),',79',font=F('Inter-Black.otf',40),fill=GOLD)
    d.text((X+wv+4,700),'/mês',font=F('Inter-Bold.otf',28),fill=GOLD)
    d.text((X,760),'Comércio, indústria,',font=F('Inter-Black.otf',27),fill=GREEN)
    d.text((X,800),'fazenda e condomínio',font=F('Inter-Bold.otf',27),fill=GREEN)
    d.text((X,880),'Veja a sua usina  →',font=F('Inter-Black.otf',40),fill=WHITE)
    rodape(c,f'*Oferta válida de {VAL}. R$ 935,79/mês: sistema de 3.000 kWh em 120x, taxa de referência 1,55% ao mês, total a prazo R$ 112.294,80; preço à vista no Pix R$ 48.300. Parcelas sujeitas à aprovação de crédito, aos critérios de cada financeira, ao score e à capacidade de pagamento de cada CPF/CNPJ. Preço por sistema individual, sujeito a análise técnica.')
    c.save('out/empresas/00_capa.jpg',quality=92)

def final():
    c=base('robo_apontando_placas.png'); logo(c); d=ImageDraw.Draw(c); X=56
    f=F('InterDisplay-Black.otf',70)
    for i,t in enumerate(['Sua conta','é maior?']): d.text((X,230+i*80),t,font=f,fill=WHITE)
    f2=F('Inter-SemiBold.otf',32)
    for i,t in enumerate(['Empresa, comércio','e agro também.','Mande a foto da sua','conta de luz e receba','o seu orçamento.']):
        d.text((X,430+i*44),t,font=f2,fill=SOFT)
    d.rounded_rectangle([X,700,X+430,800],radius=18,fill=GREEN)
    d.text((X+215,750),'(73) 3223-5102',font=F('Inter-Black.otf',40),fill=(4,14,34),anchor='mm')
    d.text((X,830),'O tempo prova.',font=F('Inter-Black.otf',38),fill=GOLD)
    rodape(c,f'Oferta válida de {VAL}. Parcelas sujeitas à aprovação de crédito, aos critérios de cada financeira, ao score e à capacidade de pagamento de cada CPF/CNPJ.')
    c.save('out/empresas/07_final.jpg',quality=92)

K=[dict(kwh=3000,placas=41,kwp='25,42',tab=50840,p12=4236.67,p60=1254.77,p84=1029.58,p120=935.79,pix=48300),
   dict(kwh=5000,placas=68,kwp='42,16',tab=82210,p12=6850.83,p60=2029.01,p84=1664.86,p120=1513.20,pix=78100),
   dict(kwh=10000,placas=135,kwp='83,70',tab=154850,p12=12904.17,p60=3821.83,p84=3135.91,p120=2850.26,pix=147110),
   dict(kwh=20000,placas=269,kwp='166,78',tab=300200,p12=25016.67,p60=7409.19,p84=6079.44,p120=5525.65,pix=285190)]
capa()
for i,k in enumerate(K,1): card(i,k)
final()
