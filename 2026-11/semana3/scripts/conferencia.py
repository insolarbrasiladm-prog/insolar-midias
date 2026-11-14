import json, glob, collections, re
us = []
for f in glob.glob('/home/claude/semana16/tmp/usos_*.json'): us += json.load(open(f))
# normaliza post: r16a->R16, bd16->BD16, feed16->F16, ch17->CH17
def post(p):
    m = re.match(r'([a-z]+?)(\d+)', p); return (m.group(1), m.group(2)) if m else (p, '')
seen = {}
for u in us:
    seen[(u['post'], u['src'], u['ss'], u['dur'])] = u
us = list(seen.values())
erros = []
imgs = collections.defaultdict(set)
for u in us:
    if u['ss'] is None: imgs[u['src']].add(u['post'])
for src, ps in imgs.items():
    if len(ps) > 1: erros.append(f'IMAGEM REPETIDA: {src} em {sorted(ps)}')
vids = collections.defaultdict(list)
for u in us:
    if u['ss'] is not None: vids[u['src']].append((u['ss'], u['ss'] + u['dur'], u['post']))
for src, segs in vids.items():
    segs.sort()
    for a, b in zip(segs, segs[1:]):
        if b[0] < a[1] and a[2] != b[2]: erros.append(f'TRECHO REPETIDO: {src} {a} x {b}')
obra = collections.defaultdict(set)
for u in us:
    if u['src'].startswith('obra-'): obra[post(u['post'])[1]].add(post(u['post'])[0])
for dia, tipos in obra.items():
    if len(tipos) > 1: erros.append(f'MAIS DE 1 POST DE OBRA NO DIA {dia}: {tipos}')
print('Materiais conferidos:', len(us), '| imagens diferentes:', len(imgs), '| vídeos:', len(vids))
print('\n'.join(erros) if erros else 'NENHUMA REPETIÇÃO ENCONTRADA')
json.dump(sorted(us, key=lambda u: u['post']), open('/home/claude/semana16/conferencia.json', 'w'), ensure_ascii=False, indent=0)
