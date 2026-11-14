import sys; sys.path.insert(0, '/home/claude/semana16')
from motor import *
P = UP + '5789a39f-579a252a-fae3-41b1-b7c1-8bde8deca5a1.mov'
SOM = TMP + 'som_bomdia.m4a'
if not os.path.exists(SOM):
    run(['ffmpeg', '-v', 'error', '-y', '-i', REPO + '2026-10/campanha/v2/reels/reel_toda_bahia.mp4', '-vn', '-c:a', 'aac', SOM])
S = simbolo(70)

def centro(d, t, y, f, col):
    w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=col)

def marca(c, y):
    d = ImageDraw.Draw(c); f1 = F('InterDisplay-Black.otf', 40); f2 = F('Inter-Bold.otf', 18)
    tw = d.textlength('INSOLAR', font=f1); x = int((W - (S.width + 14 + tw)) / 2)
    c.alpha_composite(S, (x, y)); d.text((x + S.width + 14, y + 4), 'INSOLAR', font=f1, fill=WHITE)
    d.text((x + S.width + 16, y + 50), 'BRASIL · ENERGIA SOLAR', font=f2, fill=GOLD)

BOMDIA = [
    ('16', UP + 'IMG_4770.mov', 0.5, False, 'Bom dia!', 'As misericórdias do Senhor se renovam a cada manhã.', 'Lamentações 3:22-23'),
    ('17', P, 50, True, 'Bom dia!', 'Este é o dia que o Senhor fez; alegremo-nos e regozijemo-nos nele.', 'Salmos 118:24'),
    ('18', UP + 'IMG_4770.mov', 41, False, 'Bom dia!', 'Os que esperam no Senhor renovam as suas forças.', 'Isaías 40:31'),
    ('19', P, 2, True, 'Bom dia!', 'Tudo posso naquele que me fortalece.', 'Filipenses 4:13'),
    ('20', UP + 'IMG_4770.mov', 10, False, 'Bom dia!', 'Entrega o teu caminho ao Senhor, confia nele, e ele tudo fará.', 'Salmos 37:5'),
    ('21', UP + 'IMG_4770.mov', 20, False, 'Bom sábado!', 'Consagre ao Senhor tudo o que você faz, e os seus planos serão bem-sucedidos.', 'Provérbios 16:3'),
    ('22', P, 28, True, 'Bom domingo!', 'Se alguém está em Cristo, é nova criação. As coisas antigas já passaram.', '2 Coríntios 5:17'),
]

def bomdia(dia, src, ss, land, tit, txt, ref):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    for y in range(820, H):
        dg.line([(0, y), (W, y)], fill=(5, 10, 25, min(215, int((y - 820) * 0.42))))
    c.alpha_composite(g); d = ImageDraw.Draw(c)
    fr = F('Inter-Bold.otf', 30); ft = FL(104); fv = FL(62)
    centro(d, ref.upper(), 960, fr, GOLD)
    centro(d, tit, 1010, ft, WHITE)
    y = 1170
    for ln in wrap(d, '“' + txt + '”', fv, 900):
        centro(d, ln, y, fv, WHITE); y += 82
    y += 30
    fb = F('InterDisplay-Black.otf', 40); t = 'Responda: Amém'
    w = d.textlength(t, font=fb); d.rounded_rectangle([(W - w) / 2 - 34, y, (W + w) / 2 + 34, y + 76], radius=38, fill=GOLD)
    d.text(((W - w) / 2, y + 14), t, font=fb, fill=NAVY)
    marca(c, 1640)
    ov = TMP + f'bd{dia}.png'; c.save(ov)
    o = OUT + f'story_bomdia_{dia}-11.mp4'; dur = 7
    if land:
        vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3[bg];"
              f"[b]scale=1260:-2,crop=1080:ih:'(iw-1080)*t/{dur}':0[fg];[bg][fg]overlay=0:180[v0];[v0][1:v]overlay=0:0,fps=30,format=yuv420p")
    else:
        vf = (f"[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,crop=1080:1920:'108*t/{dur}':60[v0];"
              f"[v0][1:v]overlay=0:0,fps=30,format=yuv420p")
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-loop', '1', '-i', ov, '-i', SOM,
         '-filter_complex', vf + f";[2:a]atrim=0:{dur},afade=t=in:d=0.4,afade=t=out:st={dur-1}:d=1[a]",
         '-map', '[v0]' if False else '0:v', '-t', str(dur)] if False else
        ['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-loop', '1', '-i', ov, '-i', SOM,
         '-filter_complex', vf.replace('format=yuv420p', 'format=yuv420p[v]') + f";[2:a]atrim=0:{dur},afade=t=in:d=0.4,afade=t=out:st={dur-1}:d=1[a]",
         '-map', '[v]', '-map', '[a]', '-t', str(dur), '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-c:a', 'aac', '-movflags', '+faststart', o])
    print('OK', o)

def foto_fit(src, w, h):
    im = Image.open(src).convert('RGB')
    bg = im.resize((w, h)).filter(ImageFilter.GaussianBlur(30))
    r = min(w / im.width, h / im.height) * 0.94
    fg = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    bg.paste(fg, ((w - fg.width) // 2, (h - fg.height) // 2)); return bg.convert('RGBA')

def robo_inset(src, box, size):
    im = Image.open(src).convert('RGB').crop(box).resize(size, Image.LANCZOS).convert('RGBA')
    m = Image.new('L', size, 0); ImageDraw.Draw(m).rounded_rectangle([0, 0, size[0], size[1]], radius=36, fill=255)
    im.putalpha(m); return im

def botao(d, y, t='WhatsApp (73) 3223-5102', size=44):
    f = F('InterDisplay-Black.otf', size); w = d.textlength(t, font=f)
    d.rounded_rectangle([(W - w) / 2 - 40, y, (W + w) / 2 + 40, y + size * 2.2], radius=size, fill=GOLD)
    d.text(((W - w) / 2, y + size * 0.45), t, font=f, fill=NAVY)

def tempo_prova(dia, foto, local):
    c = Image.new('RGBA', (W, H), NAVY + (255,))
    bg = Image.open(foto).convert('RGB').resize((W, H)).filter(ImageFilter.GaussianBlur(35)).convert('RGBA')
    c.alpha_composite(bg); c.alpha_composite(Image.new('RGBA', (W, H), (5, 10, 25, 120)))
    d = ImageDraw.Draw(c)
    centro(d, 'O TEMPO PROVA', 200, F('InterDisplay-Black.otf', 92), GOLD)
    centro(d, 'Obra real da Insolar', 310, F('Inter-Bold.otf', 40), WHITE)
    fp = foto_fit(foto, 980, 700)
    fr = Image.new('RGBA', (1000, 720), GOLD + (255,)); fr.alpha_composite(fp, (10, 10)); c.alpha_composite(fr, (40, 400))
    centro(d, local, 1150, F('InterDisplay-Black.otf', 50), WHITE)
    ins = robo_inset(REPO + 'robo-oficial/poses/apontando.png', (180, 180, 720, 900), (380, 507))
    c.alpha_composite(ins, (60, 1250))
    fq = F('InterDisplay-Black.otf', 56)
    y = 1330
    for ln in ['Sua casa', 'pode ser', 'a próxima.']:
        d.text((480, y), ln, font=fq, fill=WHITE); y += 72
    d.text((480, y + 16), 'Fale com a Insolar', font=F('Inter-Bold.otf', 34), fill=GOLD)
    marca(c, 1790)
    o = OUT + f'story_tempoprova_{dia}-11.png'; c.convert('RGB').save(o, quality=92); print('OK', o)

def chamada(dia, robo, t1, t2):
    c = Image.open(robo).convert('RGB').resize((W, H), Image.LANCZOS).convert('RGBA')
    g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
    for y in range(1050, H): dg.line([(0, y), (W, y)], fill=(5, 10, 25, min(225, int((y - 1050) * 0.6))))
    c.alpha_composite(g); d = ImageDraw.Draw(c)
    y = faixa(c, t1, 1280, 74, (249, 185, 30, 245), NAVY)
    y = faixa(c, t2, y + 16, 56)
    botao(d, y + 30); marca(c, 1780)
    o = OUT + f'story_chamada_{dia}-11.png'; c.convert('RGB').save(o, quality=92); print('OK', o)

def feed_card(path, img, titulo=None, sub=None, robo_full=False, last=False):
    w, h = 1080, 1350
    if robo_full:
        im = Image.open(img).convert('RGB'); r = w / im.width
        im = im.resize((w, int(im.height * r)), Image.LANCZOS).crop((0, 120, w, 120 + h)).convert('RGBA')
        c = im
    else:
        src = Image.open(img).convert('RGB')
        m = src.point(lambda v: 255 if v > 235 else 0).convert('L')
        m = Image.eval(m, lambda v: v)
        r_, g_, b_ = src.split()
        from PIL import ImageChops
        mask = ImageChops.multiply(ImageChops.multiply(r_.point(lambda v: 255 if v > 235 else 0), g_.point(lambda v: 255 if v > 235 else 0)), b_.point(lambda v: 255 if v > 235 else 0))
        bb = mask.getbbox(); fr = src.crop(bb)
        bg = src.resize((w, h)).filter(ImageFilter.GaussianBlur(30))
        rr = (w - 60) / fr.width; fr = fr.resize((w - 60, int(fr.height * rr)), Image.LANCZOS)
        bg.paste(fr, (30, (h - fr.height) // 2)); c = bg.convert('RGBA')
    if titulo or sub or last:
        g = Image.new('RGBA', (w, h), (0, 0, 0, 0)); dg = ImageDraw.Draw(g)
        for y in range(700, h): dg.line([(0, y), (w, y)], fill=(5, 10, 25, min(220, int((y - 700) * 0.5))))
        c.alpha_composite(g)
    d = ImageDraw.Draw(c)
    y = 930
    if titulo:
        for ln in wrap(d, titulo, F('InterDisplay-Black.otf', 70), 940):
            ww = d.textlength(ln, font=F('InterDisplay-Black.otf', 70)); d.text(((w - ww) / 2, y), ln, font=F('InterDisplay-Black.otf', 70), fill=WHITE); y += 84
    if sub:
        ww = d.textlength(sub, font=F('Inter-Bold.otf', 36)); d.text(((w - ww) / 2, y + 6), sub, font=F('Inter-Bold.otf', 36), fill=GOLD); y += 60
    if last:
        f = F('InterDisplay-Black.otf', 42); t = 'WhatsApp (73) 3223-5102'; ww = d.textlength(t, font=f)
        d.rounded_rectangle([(w - ww) / 2 - 40, y + 20, (w + ww) / 2 + 40, y + 112], radius=46, fill=GOLD)
        d.text(((w - ww) / 2, y + 38), t, font=f, fill=NAVY)
    d.rectangle([0, h - 10, w, h], fill=GOLD)
    c.convert('RGB').save(path, quality=92)

if __name__ == '__main__':
    for b in BOMDIA:
        if b[0] in sys.argv[1:] or not sys.argv[1:]: bomdia(*b)
    tempo_prova('16', OBRA + 'obra-ilheus-metalico-serra.jpg', 'Ilhéus · Telhado metálico')
    tempo_prova('19', OBRA + 'obra-jequie-solo-eucalipto.jpg', 'Jequié · Usina no solo')
    chamada('17', REPO + 'robo-oficial/poses/joinha.png', 'Conta de luz chegou alta?', 'A Insolar faz a simulação do seu sistema.')
    os.makedirs(OUT + 'feed16', exist_ok=True); os.makedirs(OUT + 'feed20', exist_ok=True)
    feed_card(OUT + 'feed16/1.jpg', REPO + 'robo-oficial/poses/entrega_documentos_casal.png', 'Obras reais da Insolar', 'Arraste e veja ›', robo_full=True)
    for i, f in enumerate(['obra-ilheus-ceramica-aerea.jpg', 'obra-ilheus-residencial-aerea.jpg', 'obra-ilheus-metalico-aerea.jpg', 'obra-ilheus-residencial-aerea-2.jpg', 'obra-ilheus-ceramica-aeroporto.jpg'], 2):
        feed_card(OUT + f'feed16/{i}.jpg', OBRA + f)
    feed_card(OUT + 'feed16/7.jpg', REPO + 'robo-oficial/poses/mao_peito.png', 'Sua casa pode ser a próxima.', None, robo_full=True, last=True)
    feed_card(OUT + 'feed20/1.jpg', REPO + 'robo-oficial/poses/apontando.png', 'A Insolar está em toda a Bahia', 'Arraste e veja ›', robo_full=True)
    for i, f in enumerate(['obra-jequie-solo-eucalipto.jpg', 'obra-marau-usina-solo.jpg', 'obra-salvador-telhado-metalico.jpg', 'obra-ilheus-metalico-serra.jpg', 'obra-ilheus-residencial-aerea-3.jpg'], 2):
        feed_card(OUT + f'feed20/{i}.jpg', OBRA + f)
    feed_card(OUT + 'feed20/7.jpg', REPO + 'robo-oficial/poses/acenando.png', 'De Ilhéus para toda a Bahia.', 'Mais de 7 anos de experiência', robo_full=True, last=True)
    print('feeds OK')
