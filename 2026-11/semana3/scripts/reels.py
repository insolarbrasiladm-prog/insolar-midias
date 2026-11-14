import sys; sys.path.insert(0, '/home/claude/semana16')
from motor import *
A = REPO + 'trilhas/trilha_insolar_02_animada.mp3'
C = REPO + 'trilhas/trilha_insolar_03_criancas.mp3'
R = ROBO; O = OBRA
which = sys.argv[1:] or ['1', '2', '3', '4', '5', '6', '7']

if '1' in which:  # Seg 16 - ponte
    s = [seg_video('r1a', UP + 'IMG_4772.mov', 27, 2.2, [('faixa', 'Todo dia milhares de pessoas atravessam esta ponte…', 1180, 70)]),
         seg_video('r1b', UP + 'IMG_4772.mov', 36, 2.0, [('faixa', '…e quase ninguém repara', 1180, 70)]),
         seg_img('r1c', O + 'obra-ilheus-residencial-aerea.jpg', 2.0, [('gold', 'quantos telhados de Ilhéus já geram a própria energia', 1180, 62)]),
         seg_img('r1d', O + 'obra-ilheus-ceramica-aerea.jpg', 1.8, [('faixa', 'Obras reais. Clientes reais.', 1180, 66)], zoom='out'),
         seg_img('r1e', R + '1_seg16_robo_casal_aperto_de_mao.png', 2.6, [('faixa', 'O próximo telhado pode ser o seu.', 1250, 70)]),
         seg_final('r1f')]
    juntar('reel_16-11_ponte', s, A)

if '2' in which:  # Ter 17 - 3 coisas
    s = [seg_img('r2a', R + '2_ter17_robo_tablet_varanda.png', 2.4, [('faixa', '3 coisas para conferir antes de fechar energia solar 👇'.replace(' 👇', ''), 1230, 70)]),
         seg_img('r2b', O + 'obra-marau-usina-solo.jpg', 2.6, [('gold', '1. Nota fiscal do equipamento no SEU nome', 1180, 64)]),
         seg_img('r2c', O + 'obra-ilheus-metalico-aerea.jpg', 2.6, [('gold', '2. Instalação homologada na Coelba', 1180, 64)], zoom='out'),
         seg_img('r2d', O + 'obra-ilheus-residencial-aerea-2.jpg', 2.6, [('gold', '3. Obras reais para te mostrar', 1180, 64)]),
         seg_img('r2e', R + '2_ter17_robo_tablet_varanda.png', 2.2, [('faixa', 'Na Insolar, as 3 vêm de série.', 1250, 70)], zoom='out'),
         seg_final('r2f')]
    juntar('reel_17-11_3coisas', s, A)

if '3' in which:  # Qua 18 - por do sol
    P = UP + '5789a39f-579a252a-fae3-41b1-b7c1-8bde8deca5a1.mov'
    s = [seg_video('r3a', P, 0.5, 2.6, [('faixa', 'Ilhéus tem um dos pores do sol mais bonitos da Bahia', 1250, 68)], land=True),
         seg_video('r3b', P, 22, 2.4, [('faixa', 'O céu muda de cor…', 1250, 68)], land=True),
         seg_video('r3c', P, 44, 2.2, [('faixa', '…e o sol trabalha o ano inteiro', 1250, 68)], land=True),
         seg_img('r3d', R + '3_qua18_robo_orla_por_do_sol.png', 3.0, [('gold', 'Aqui, o sol trabalha para você.', 1250, 66)]),
         seg_final('r3e')]
    juntar('reel_18-11_por_do_sol', s, A)

if '4' in which:  # Qui 19 - criancas
    K = R + '4_qui19_robo_criancas_quintal_sem_escudo.png'
    s = [seg_img('r4a', K, 2.6, [('faixa', 'O que você vai deixar para os seus filhos?', 1300, 70)]),
         seg_img('r4b', O + 'obra-ilheus-residencial-aerea-3.jpg', 2.2, [('faixa', 'Uma casa que gera a própria energia', 1180, 66)]),
         seg_img('r4c', O + 'obra-ilheus-ceramica-aeroporto.jpg', 2.2, [('gold', 'Placas com 25 anos de garantia de desempenho', 1180, 62)], zoom='out'),
         seg_img('r4d', K, 2.6, [('faixa', 'Pense no futuro deles.', 1300, 70)], zoom='out'),
         seg_final('r4e')]
    juntar('reel_19-11_criancas', s, C)

if '5' in which:  # Sex 20 - Ilheus a noite + contagem
    s = [seg_video('r5a', UP + 'IMG_4820.mov', 0.3, 2.2, [('faixa', 'Sexta à noite em Ilhéus', 1250, 74)]),
         seg_video('r5b', UP + 'IMG_4558.mov', 3, 2.2, [], pan='y'),
         seg_video('r5c', UP + 'IMG_4553.mov', 7.5, 2.0, []),
         seg_video('r5d', UP + 'IMG_4557.mov', 16, 2.0, [], pan='y'),
         seg_img('r5e', R + '5_sex20_robo_cidade_noite_ponte.png', 3.0, [('gold', 'Faltam 7 dias para a Black Friday', 1250, 66), ('faixa', 'Já escolheu o seu presente?', 1500, 62)]),
         seg_final('r5f')]
    juntar('reel_20-11_ilheus_noite', s, A)

if '6' in which:  # Sab 21 - bastidores
    s = [seg_img('r6a', R + '6_sab21_robo_caixas_nota_fiscal.png', 2.6, [('faixa', 'O que ninguém te mostra antes da instalação', 1300, 68)]),
         seg_video('r6b', REPO + 'videos-ia/caixas_abrindo.mp4', 5.0, 2.4, [('faixa', 'Material conferido, item por item', 1250, 66)]),
         seg_img('r6c', R + '6_sab21_robo_caixas_nota_fiscal.png', 2.4, [('gold', 'Nota fiscal no SEU nome', 1300, 70)], zoom='out'),
         seg_img('r6d', O + 'obra-salvador-telhado-metalico.jpg', 2.4, [('faixa', 'Só depois disso, o telhado.', 1180, 68)]),
         seg_final('r6e')]
    juntar('reel_21-11_bastidores', s, A)

if '7' in which:  # Dom 22 - vista do alto
    s = [seg_video('r7a', UP + 'IMG_4770.mov', 1, 3.0, [('faixa', 'Domingo de sol em Ilhéus', 1250, 74)]),
         seg_video('r7b', UP + 'IMG_4770.mov', 40, 2.4, []),
         seg_video('r7c', UP + 'IMG_4772.mov', 31, 2.2, [('faixa', 'Cada telhado desses pode gerar energia', 1250, 66)]),
         seg_img('r7d', REPO + 'robo-oficial/poses/sentado_limpo.png', 3.0, [('gold', 'Bom domingo! O sol já está trabalhando.', 1250, 64)]),
         seg_final('r7e')]
    juntar('reel_22-11_domingo', s, A)
