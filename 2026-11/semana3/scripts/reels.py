import sys; sys.path.insert(0, '/home/claude/semana16')
from motor import *
A = REPO + 'trilhas/trilha_insolar_02_animada.mp3'
C = REPO + 'trilhas/trilha_insolar_03_criancas.mp3'
R = ROBO; O = OBRA; PO = REPO + 'robo-oficial/poses/'; BK = REPO + '2026-11/black/'; IA = REPO + 'videos-ia/'
PDS = UP + '5789a39f-579a252a-fae3-41b1-b7c1-8bde8deca5a1.mov'
BLACK = 'BLACK NOVEMBRO · ESCOLHA O SEU PRESENTE'
w = sys.argv[1:]

if '16' in w:
    juntar('reel_16-11_ponte', [
        seg_video('r16a', UP + 'IMG_4772.mov', 36, 2.2, [('faixa', 'Todo dia milhares de pessoas atravessam esta ponte…', 1180, 70)]),
        seg_video('r16b', UP + 'IMG_4772.mov', 44, 2.0, [('faixa', '…e quase ninguém repara', 1180, 70)]),
        seg_img('r16c', O + 'obra-ilheus-residencial-aerea.jpg', 2.0, [('gold', 'quantos telhados de Ilhéus já geram a própria energia', 1180, 62)]),
        seg_img('r16d', O + 'obra-ilheus-ceramica-aerea.jpg', 1.8, [('faixa', 'Obras reais. Clientes reais.', 1180, 66)], zoom='out'),
        seg_img('r16e', R + '1_seg16_robo_casal_aperto_de_mao.png', 2.6, [('faixa', 'O próximo telhado pode ser o seu.', 1250, 70)]),
        seg_final('f16')], A)
if '17' in w:
    juntar('reel_17-11_3coisas', [
        seg_img('r17a', R + '2_ter17_robo_tablet_varanda.png', 2.4, [('faixa', '3 coisas para conferir antes de fechar energia solar', 1230, 70)]),
        seg_img('r17b', O + 'obra-ilheus-metalico-serra.jpg', 2.6, [('gold', '1. Nota fiscal do equipamento no SEU nome', 1180, 64)]),
        seg_img('r17c', O + 'obra-ilheus-metalico-aerea.jpg', 2.6, [('gold', '2. Instalação homologada na Coelba', 1180, 64)], zoom='out'),
        seg_img('r17d', O + 'obra-ilheus-residencial-aerea-2.jpg', 2.6, [('gold', '3. Obras reais para te mostrar', 1180, 64)]),
        seg_final('f17', 'NA INSOLAR, AS 3 VÊM DE SÉRIE')], A)
if '18' in w:
    juntar('reel_18-11_por_do_sol', [
        seg_video('r18a', PDS, 0.5, 2.6, [('faixa', 'Ilhéus tem um dos pores do sol mais bonitos da Bahia', 1250, 68)], land=True),
        seg_video('r18b', PDS, 22, 2.4, [('faixa', 'O céu muda de cor…', 1250, 68)], land=True),
        seg_video('r18c', PDS, 44, 2.2, [('faixa', '…e o sol trabalha o ano inteiro', 1250, 68)], land=True),
        seg_img('r18d', R + '3_qua18_robo_orla_por_do_sol.png', 3.0, [('gold', 'Aqui, o sol trabalha para você.', 1250, 66)]),
        seg_final('f18')], A)
if '19' in w:
    K = R + '4_qui19_robo_criancas_quintal_sem_escudo.png'
    juntar('reel_19-11_criancas', [
        seg_img('r19a', K, 2.8, [('faixa', 'O que você vai deixar para os seus filhos?', 1300, 70)]),
        seg_img('r19b', O + 'obra-ilheus-residencial-aerea-3.jpg', 2.4, [('faixa', 'Uma casa que gera a própria energia', 1180, 66)]),
        seg_img('r19c', O + 'obra-ilheus-ceramica-aeroporto.jpg', 2.4, [('gold', 'Placas com 25 anos de garantia de desempenho', 1180, 62)], zoom='out'),
        seg_final('f19', 'PENSE NO FUTURO DELES')], C)
if '20' in w:
    juntar('reel_20-11_ilheus_noite', [
        seg_video('r20a', UP + 'IMG_4820.mov', 0.3, 2.2, [('faixa', 'Sexta à noite em Ilhéus', 1250, 74)]),
        seg_video('r20b', UP + 'IMG_4558.mov', 3, 2.2, [], pan='y'),
        seg_video('r20c', UP + 'IMG_4553.mov', 7.5, 2.0, []),
        seg_video('r20d', UP + 'IMG_4557.mov', 16, 2.0, [], pan='y'),
        seg_img('r20e', R + '5_sex20_robo_cidade_noite_ponte.png', 3.0, [('gold', 'Faltam 7 dias para a Black Friday', 1250, 66), ('faixa', 'Já escolheu o seu presente?', 1500, 62)]),
        seg_final('f20')], A)
if '21' in w:
    juntar('reel_21-11_bastidores', [
        seg_img('r21a', R + '6_sab21_robo_caixas_nota_fiscal.png', 3.0, [('faixa', 'O que ninguém te mostra antes da instalação', 1300, 68)]),
        seg_video('r21b', IA + 'caixas_abrindo.mp4', 5.0, 2.6, [('faixa', 'Material conferido, item por item', 1250, 66)]),
        seg_video('r21c', IA + 'caixas_abrindo.mp4', 7.6, 2.4, [('gold', 'Nota fiscal no SEU nome', 1300, 70)]),
        seg_final('f21', 'SÓ DEPOIS DISSO, O TELHADO')], A)
if '22' in w:
    juntar('reel_22-11_domingo', [
        seg_video('r22a', UP + 'IMG_4770.mov', 36, 3.0, [('faixa', 'Domingo de sol em Ilhéus', 1250, 74)]),
        seg_video('r22b', UP + 'IMG_4770.mov', 42, 2.6, [('faixa', 'Cada telhado desses pode gerar energia', 1250, 66)]),
        seg_img('r22c', PO + 'sentado_limpo.png', 3.0, [('gold', 'Bom domingo! O sol já está trabalhando.', 1250, 64)]),
        seg_final('f22')], A)
# ---------- semana 23 a 30 ----------
if '23' in w:
    juntar('reel_23-11_barato_demais', [
        seg_img('r23a', BK + 'base_robo_apontando.png', 2.6, [('faixa', 'Orçamento barato demais? Cuidado.', 1250, 76)]),
        seg_video('r23b', IA + 'zoom_satelite_casal.mp4', 0, 3.0, [('faixa', 'Energia solar é para durar mais de 20 anos', 1250, 66)]),
        seg_img('r23c', PO + 'caixas_entrega_com_logo.png', 3.0, [('gold', 'Confira o material, a nota fiscal e a homologação', 1250, 62)]),
        seg_final('f23', 'TRAGA O SEU ORÇAMENTO: NÓS COBRIMOS*')], A)
if '24' in w:
    juntar('reel_24-11_luz_caiu', [
        seg_img('r24b', PO + 'bateria_garagem_noite.png', 3.2, [('faixa', 'A luz da rua caiu. E a sua casa continua acesa?', 1250, 70)]),
        seg_img('r24c', PO + 'bateria_garagem_noite.png', 2.6, [('gold', 'Com bateria, o sol de hoje vira a luz da noite', 1250, 62)], zoom='out'),
        seg_final('f24', 'BATERIAS TAMBÉM ENTRAM NO BLACK NOVEMBRO')], A)
if '25' in w:
    juntar('reel_25-11_comercio', [
        seg_img('r25a', PO + 'empresa_padaria.png', 2.8, [('faixa', 'Seu comércio liga cedo e fecha tarde?', 1250, 72)]),
        seg_img('r25b', PO + 'empresa_padaria.png', 2.8, [('gold', 'Padaria, mercado, oficina, pousada', 1300, 66)], zoom='out'),
        seg_final('f25', 'ENERGIA SOLAR PARA O SEU NEGÓCIO')], A)
if '26' in w:
    juntar('reel_26-11_amanha_black', [
        seg_video('r26a', UP + 'IMG_4552.mov', 4, 2.4, [('faixa', 'Amanhã é Black Friday', 1250, 78)]),
        seg_video('r26b', UP + 'IMG_4558.mov', 10, 2.2, [], pan='y'),
        seg_img('r26c', PO + 'ponte_jorge_amado_noite.png', 3.0, [('gold', 'Traga o seu melhor preço: nós cobrimos*', 1250, 64), ('faixa', 'E ainda escolha o seu presente', 1480, 60)]),
        seg_final('f26')], A)
if '27' in w:
    juntar('reel_27-11_black_friday', [
        seg_video('r27a', IA + 'robo_presente_black.mp4', 0, 3.0, [('gold', 'É HOJE: Black Friday Insolar', 1300, 74)]),
        seg_img('r27b', PO + 'presente_black.png', 3.0, [('faixa', 'Escolha o seu presente', 1250, 70), ('faixa', 'limpeza · inspeção · +1 ano de garantia', 1420, 50)]),
        seg_final('f27', 'VÁLIDO ATÉ 30/11 · CONDIÇÕES NO WHATSAPP')], A)
if '28' in w:
    juntar('reel_28-11_vizinho', [
        seg_img('r28a', PO + 'indicacao_vizinhos.png', 3.0, [('faixa', 'Seu vizinho já gera a própria energia?', 1300, 70)]),
        seg_img('r28b', PO + 'indicacao_vizinhos.png', 2.8, [('gold', 'Só faltam 3 dias do Black Novembro', 1300, 66)], zoom='out'),
        seg_final('f28')], A)
if '29' in w:
    juntar('reel_29-11_termina_amanha', [
        seg_video('r29a', IA + 'robo_caixas_insolar.mp4', 0, 3.0, [('faixa', 'Termina amanhã', 1300, 80)]),
        seg_img('r29b', BK + 'base_robo_joinha.png', 3.0, [('gold', 'Último fim de semana do Black Novembro', 1250, 64)]),
        seg_final('f29')], A)
if '30' in w:
    juntar('reel_30-11_ultimo_dia', [
        seg_img('r30a', BK + 'base_robo_presente.png', 2.6, [('faixa', 'Último dia.', 1250, 84)]),
        seg_img('r30b', BK + 'base_robo_presente.png', 2.6, [('gold', 'Hoje é a última chance do Black Novembro', 1250, 64)], zoom='out'),
        seg_final('f30', 'SÓ HOJE, 30/11 · CHAME NO WHATSAPP')], A)
