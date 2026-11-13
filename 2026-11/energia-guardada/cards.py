from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
import sys
FD = '/usr/share/fonts/opentype/inter/'
def F(n, s): return ImageFont.truetype(FD + n, s)
NAVY = (14, 42, 94); GOLD = (249, 185, 30); GREEN = (60, 200, 110); RED = (220, 40, 40); WHITE = (255, 255, 255)
UP = '/mnt/user-data/uploads/'
SIMB = Image.open('/home/claude/midias/marca/insolar_S.png').convert('RGBA')
W = 1080

def simb(h):
    return SIMB.resize((int(SIMB.width * h / SIMB.height), h), Image.LANCZOS)

def sticker(img, x, y, h, alpha=0.92):
    """símbolo da Insolar colado no gabinete da bateria (coordenadas da imagem original)."""
    s = simb(h)
    a = s.split()[3].point(lambda v: int(v * alpha))
    s.putalpha(a)
    img.alpha_composite(s, (x, y))

def grad(c, y0, y1, top_alpha, bot_alpha):
    ov = Image.new('RGBA', c.size, (0, 0, 0, 0)); d = ImageDraw.Draw(ov)
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0)
        d.line([(0, y), (W, y)], fill=(5, 10, 25, int(top_alpha + (bot_alpha - top_alpha) * t)))
    c.alpha_composite(ov)

def boxes(d, lines, x, y, f, bg, fg, align='l', lh=None):
    lh = lh or int(f.size * 1.45)
    for ln in lines:
        w = d.textlength(ln, font=f)
        x0 = x if align == 'l' else (x - w if align == 'r' else x - w / 2)
        bb = d.textbbox((x0, y), ln, font=f)
        d.rectangle([x0 - 14, y - int(f.size*0.05), x0 + w + 14, y + int(f.size * 1.24)], fill=bg)
        d.text((x0, y), ln, font=f, fill=fg)
        y += lh
    return y

def text_shadow(c, xy, txt, f, fill, anchor='la'):
    sh = Image.new('RGBA', c.size, (0, 0, 0, 0)); ds = ImageDraw.Draw(sh)
    ds.text((xy[0] + 3, xy[1] + 4), txt, font=f, fill=(0, 0, 0, 170), anchor=anchor)
    sh = sh.filter(ImageFilter.GaussianBlur(6)); c.alpha_composite(sh)
    ImageDraw.Draw(c).text(xy, txt, font=f, fill=fill, anchor=anchor)

MB = 0
def rodape(c, H, extra=None):
    H0 = H; H = H - MB
    grad(c, H - 300, H0, 0, 235)
    d = ImageDraw.Draw(c)
    s = simb(78)
    f1 = F('InterDisplay-Black.otf', 44); f2 = F('Inter-Bold.otf', 19)
    tw = max(d.textlength('INSOLAR', font=f1), d.textlength('BRASIL · ENERGIA SOLAR', font=f2))
    total = s.width + 16 + tw; x = int((W - total) / 2); y = H - 128
    c.alpha_composite(s, (x, y))
    d.text((x + s.width + 16, y + 6), 'INSOLAR', font=f1, fill=WHITE)
    d.text((x + s.width + 18, y + 54), 'BRASIL · ENERGIA SOLAR', font=f2, fill=GOLD)
    d.rectangle([0, H0 - 12, W, H0], fill=GOLD)
    if extra: extra(d)

def base(src, off, H, stickers=()):
    im = Image.open(UP + src).convert('RGBA')
    for (x, y, h) in stickers: sticker(im, x, y, h)
    s = W / im.width
    im = im.resize((W, int(im.height * s)), Image.LANCZOS)
    return im.crop((0, off, W, off + H))

def card1(H, off):
    c = base('d5b2c4e1-image.png', off, H, [(405, 890, 56)])
    grad(c, 0, 460, 170, 0)
    d = ImageDraw.Draw(c)
    text_shadow(c, (1030, 70), 'A geração', F('InterDisplay-Light.otf', 84), WHITE, 'ra')
    text_shadow(c, (1030, 160), 'é só o começo.', F('InterDisplay-Black.otf', 84), WHITE, 'ra')
    boxes(d, ['Placas, baterias e gestão de energia', 'num sistema só, para mais autonomia', 'na sua casa ou empresa.'],
          1030, 280, F('InterDisplay-Medium.otf', 30), GOLD, NAVY, 'r')
    rodape(c, H); return c

def card2(H, off):
    c = base('6acd9ffb-image.png', off, H)
    d = ImageDraw.Draw(c)
    d.text((60, 110), 'A luz caiu.', font=F('InterDisplay-Light.otf', 120), fill=WHITE)
    d.text((60, 245), 'Você, não.', font=F('InterDisplay-Black.otf', 120), fill=WHITE)
    boxes(d, ['Uma queda de energia não precisa parar', 'a sua rotina nem o seu negócio.'],
          70, 405, F('InterDisplay-Medium.otf', 33), GOLD, NAVY)
    rodape(c, H); return c

def card3(H, off):
    c = base('29786ef8-image.png', off, H, [(482, 640, 62), (672, 640, 62)])
    grad(c, 0, 470, 200, 0)
    d = ImageDraw.Draw(c)
    fl = F('InterDisplay-Light.otf', 84); fb = F('InterDisplay-Black.otf', 84)
    text_shadow(c, (540, 60), 'Bateria não é só', fl, WHITE, 'ma')
    text_shadow(c, (540, 155), 'uma caixa a mais.', fb, WHITE, 'ma')
    boxes(d, ['É a energia do sol guardada para', 'usar quando você precisar.'],
          540, 275, F('InterDisplay-Medium.otf', 32), GOLD, NAVY, 'c')
    rodape(c, H); return c

def card4(H, off):
    c = base('1082f6be-image.png', off, H, [(56, 596, 30), (119, 596, 30)])
    grad(c, 700, H, 0, 150)
    fb = F('InterDisplay-Black.otf', 76)
    text_shadow(c, (1035, 820), 'Gerar é bom.', fb, GOLD, 'ra')
    text_shadow(c, (1035, 905), 'Escolher quando', fb, WHITE, 'ra')
    text_shadow(c, (1035, 990), 'usar é melhor.', F('InterDisplay-Light.otf', 76), WHITE, 'ra')
    rodape(c, H); return c

DY = 0
def card5(H, off):
    c = base('82452dc8-image.png', off, H)
    d = ImageDraw.Draw(c)
    y = boxes(d, ['Sem energia', 'guardada.'], 1030, 820 + DY, F('InterDisplay-Black.otf', 84), RED, WHITE, 'r', 108)
    d.text((1030, y + 40), ('TOQUE PARA VER O DEPOIS ›' if DY else 'ARRASTE PARA O LADO ›'), font=F('Inter-Bold.otf', 28), fill=GREEN, anchor='ra')
    rodape(c, H); return c

def card6(H, off):
    c = base('a4995140-image.png', off, H, [(487, 300, 40), (572, 300, 40)])
    grad(c, 640 + DY, H, 0, 150)
    d = ImageDraw.Draw(c)
    y = boxes(d, ['Com energia', 'guardada.'], 1030, 700 + DY, F('InterDisplay-Black.otf', 84), GREEN, WHITE, 'r', 108)
    fb = F('Inter-Black.otf', 34); t = 'WhatsApp (73) 3223-5102'
    w = d.textlength(t, font=fb)
    d.rounded_rectangle([1030 - w - 50, y + 30, 1030, y + 102], 36, fill=GOLD)
    d.text((1030 - w - 25, y + 47), t, font=fb, fill=NAVY)
    d.text((1030, y + 122), 'Autonomia conforme o dimensionamento do sistema.', font=F('Inter-Medium.otf', 19), fill=WHITE, anchor='ra')
    d.text((1030, y + 146), 'Imagens ilustrativas criadas com IA.', font=F('Inter-Medium.otf', 19), fill=WHITE, anchor='ra')
    rodape(c, H); return c

CARDS = [(card1, 330), (card2, 300), (card3, 200), (card4, 330), (card5, 186), (card6, 130)]
if __name__ == '__main__':
    out = []
    for i, (fn, off) in enumerate(CARDS, 1):
        im = fn(1350, off).convert('RGB'); im.save(f'feed_{i}.jpg', quality=93); out.append(im)
    sheet = Image.new('RGB', (3 * 540 + 40, 2 * 675 + 30), 'white')
    for i, im in enumerate(out):
        sheet.paste(im.resize((540, 675)), (10 + (i % 3) * 550, 10 + (i // 3) * 685))
    sheet.save('prova.jpg', quality=85)
