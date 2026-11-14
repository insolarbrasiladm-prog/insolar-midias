#!/usr/bin/env python3
# Motor de montagem da semana 16 a 22/11/2026 - Insolar Brasil
import subprocess, os, sys, json
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H = 1080, 1920
NAVY = (14, 42, 94); GOLD = (249, 185, 30); GREEN = (60, 200, 110); WHITE = (255, 255, 255); BLACK = (8, 8, 12)
FD = '/usr/share/fonts/opentype/inter/'
LORA = '/usr/share/fonts/truetype/google-fonts/Lora-Italic-Variable.ttf'
REPO = '/home/claude/insolarbrasiladm-prog/insolar-midias/'
UP = '/mnt/user-data/uploads/'
ROBO = '/home/claude/semana16/robo/'
OBRA = '/home/claude/site/img/obras-reais/'
OUT = '/home/claude/semana16/saida/'
TMP = '/home/claude/semana16/tmp/'
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

def F(n, s): return ImageFont.truetype(FD + n, s)
def FL(s):
    f = ImageFont.truetype(LORA, s)
    try: f.set_variation_by_name('Bold Italic')
    except Exception: pass
    return f

def simbolo(h):
    s = Image.open(REPO + 'robo-oficial/simbolo_insolar.png').convert('RGBA')
    px = s.load()
    for y in range(s.height):
        for x in range(s.width):
            r, g, b, a = px[x, y]
            if r > 238 and g > 238 and b > 238: px[x, y] = (255, 255, 255, 0)
    bb = s.getbbox(); s = s.crop(bb)
    return s.resize((int(s.width * h / s.height), h), Image.LANCZOS)

def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print(' '.join(cmd)); print(r.stderr[-2000:]); sys.exit(1)

def wrap(d, txt, f, maxw):
    out = []
    for par in txt.split('\n'):
        ws = par.split(' '); cur = ''
        for w in ws:
            t = (cur + ' ' + w).strip()
            if d.textlength(t, font=f) <= maxw: cur = t
            else:
                if cur: out.append(cur)
                cur = w
        out.append(cur)
    return out

def faixa(c, txt, y, size=66, bg=(5, 10, 25, 200), fg=WHITE, font='InterDisplay-Black.otf', maxw=900):
    d = ImageDraw.Draw(c); f = F(font, size)
    lines = wrap(d, txt, f, maxw); lh = int(size * 1.28)
    for ln in lines:
        w = d.textlength(ln, font=f); x = (W - w) / 2
        d.rounded_rectangle([x - 26, y - 10, x + w + 26, y + lh - 2], radius=14, fill=bg)
        d.text((x, y), ln, font=f, fill=fg)
        y += lh + 8
    return y

def overlay_png(name, items):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0))
    for it in items:
        kind = it[0]
        if kind == 'faixa': faixa(c, *it[1:])
        elif kind == 'gold': faixa(c, it[1], it[2], it[3] if len(it) > 3 else 64, (249, 185, 30, 245), NAVY)
        elif kind == 'blur':
            pass
    p = TMP + name + '.png'; c.save(p); return p

# ---------- segmentos ----------
def seg_video(name, src, ss, dur, txt_items, pan='x', land=False, blur_box=None):
    ov = overlay_png(name + '_ov', txt_items)
    o = TMP + name + '.mp4'
    if land:
        vf = (f"[0:v]split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,boxblur=30:3,eq=brightness=-0.08[bg];"
              f"[b]scale=1260:-2,crop=1080:ih:'(iw-1080)*t/{dur}':0[fg];[bg][fg]overlay=0:(H-h)/2-120[v0];[v0][1:v]overlay=0:0,fps=30,format=yuv420p")
    else:
        mv = f"'108*t/{dur}'" if pan == 'x' else "54"
        my = "96" if pan == 'x' else f"'192*t/{dur}'"
        vf = (f"[0:v]scale=1188:2112:force_original_aspect_ratio=increase,crop=1188:2112,crop=1080:1920:{mv}:{my}[v0];"
              f"[v0][1:v]overlay=0:0,fps=30,format=yuv420p")
    run(['ffmpeg', '-v', 'error', '-y', '-ss', str(ss), '-t', str(dur), '-i', src, '-loop', '1', '-i', ov,
         '-filter_complex', vf, '-t', str(dur), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', o])
    return o

def prep_img(src, blur_box=None):
    im = Image.open(src).convert('RGB')
    if blur_box:
        x0, y0, x1, y1 = blur_box
        reg = im.crop(blur_box).filter(ImageFilter.GaussianBlur(9)); im.paste(reg, (x0, y0))
    # preenche 9:16
    tw, th = 2160, 3840
    r = max(tw / im.width, th / im.height)
    im2 = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    if abs(im.width / im.height - 9 / 16) > 0.05:
        bg = im.resize((tw, th)).filter(ImageFilter.GaussianBlur(40))
        r2 = tw / im.width
        fg = im.resize((tw, int(im.height * r2)), Image.LANCZOS)
        bg.paste(fg, (0, (th - fg.height) // 2 - 200)); im2 = bg
    else:
        im2 = im2.crop(((im2.width - tw) // 2, (im2.height - th) // 2, (im2.width - tw) // 2 + tw, (im2.height - th) // 2 + th))
    p = TMP + os.path.basename(src) + '_9x16.jpg'; im2.save(p, quality=92); return p

def seg_img(name, src, dur, txt_items, zoom='in', blur_box=None):
    ov = overlay_png(name + '_ov', txt_items)
    p = prep_img(src, blur_box)
    n = int(dur * 30)
    z = f"1+0.10*on/{n}" if zoom == 'in' else f"1.10-0.10*on/{n}"
    vf = (f"[0:v]zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s=1080x1920:fps=30[v0];"
          f"[v0][1:v]overlay=0:0,format=yuv420p")
    o = TMP + name + '.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-i', p, '-loop', '1', '-i', ov, '-filter_complex', vf,
         '-frames:v', str(n), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', o])
    return o

def seg_final(name, oferta='BLACK NOVEMBRO · ESCOLHA O SEU PRESENTE', dur=2.6):
    c = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    f1 = F('InterDisplay-Black.otf', 70); f2 = F('Inter-Bold.otf', 30); f3 = F('InterDisplay-Black.otf', 44)
    y = 1360
    for t, f, col in [('INSOLAR BRASIL', f1, WHITE), ('ENERGIA SOLAR · BATERIAS · SERVIÇOS', f2, GOLD)]:
        w = d.textlength(t, font=f); d.text(((W - w) / 2, y), t, font=f, fill=col); y += int(f.size * 1.4)
    y += 10
    w = d.textlength(oferta, font=f2); d.text(((W - w) / 2, y), oferta, font=f2, fill=WHITE); y += 70
    bt = 'WhatsApp (73) 3223-5102'; w = d.textlength(bt, font=f3)
    d.rounded_rectangle([(W - w) / 2 - 40, y, (W + w) / 2 + 40, y + 96], radius=48, fill=GOLD)
    d.text(((W - w) / 2, y + 20), bt, font=f3, fill=NAVY)
    ov = TMP + name + '_ov.png'; c.save(ov)
    o = TMP + name + '.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-sseof', str(-dur), '-i', REPO + 'videos-ia/logo_abertura.mp4', '-loop', '1', '-i', ov,
         '-filter_complex', "[0:v]scale=1080:1920,crop=1080:1920:0:0[v0];[v0][1:v]overlay=0:0,fps=30,format=yuv420p",
         '-t', str(dur), '-an', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '20', o])
    return o

def juntar(nome, segs, trilha):
    lst = TMP + nome + '_lista.txt'
    open(lst, 'w').write(''.join(f"file '{s}'\n" for s in segs))
    tot = sum(float(subprocess.run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'csv=p=0', s], capture_output=True, text=True).stdout) for s in segs)
    o = OUT + nome + '.mp4'
    run(['ffmpeg', '-v', 'error', '-y', '-f', 'concat', '-safe', '0', '-i', lst, '-stream_loop', '-1', '-i', trilha,
         '-filter_complex', f"[1:a]atrim=0:{tot},afade=t=in:d=0.3,afade=t=out:st={tot-0.9}:d=0.9,volume=0.9[a]",
         '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '21', '-c:a', 'aac', '-b:a', '128k',
         '-t', str(tot), '-movflags', '+faststart', o])
    print('OK', o, round(tot, 1), 's')
    return o
