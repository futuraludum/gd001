# Importação da blbioteca
import random

# Título do jogo
TITLE = 'Voando na Caverna'
# Largura da janela
WIDTH = 800
# Altura da janela
HEIGHT = 679

music.play('cant_stop_my_feet')

# Esta função executa em torno de 60 vezes por segundo
def update():
    if (morcego.started):
        morcego.speed += gravidade
        morcego.y += morcego.speed
        estalactite1.x -= morcego.velocidade_tela
        estalagmite1.x -= morcego.velocidade_tela

        estalactite2.x -= morcego.velocidade_tela
        estalagmite2.x -= morcego.velocidade_tela

        # Condição para verificar se a estalactite atingiu uma posição negativa no eixo x
        if (estalactite1.x) < 0:
            ajuste = random.randint(-80, 80)
            estalactite1.midleft = (WIDTH, ajuste)
            estalagmite1.midleft = (WIDTH, ajuste + estalactite1.height + espaco)
            estalactite1.number += 1

        if (estalactite2.x) < 0:
            ajuste = random.randint(-80, 80)
            estalactite2.midleft = (WIDTH, ajuste)
            estalagmite2.midleft = (WIDTH, ajuste + estalactite2.height + espaco)
            estalactite2.number += 1

        # Condição para verificar se o morcego atingiu o topo ou o chão da caverna
        if (morcego.y > HEIGHT):
            reset()

        # Condição que verifica a colisão nos obstáculos
        if ((morcego.colliderect(estalactite1)) or (morcego.colliderect(estalagmite1)) or (morcego.y <= 0)
            or (morcego.colliderect(estalactite2)) or (morcego.colliderect(estalagmite2))):
            colisao()

        # Condição que verifica se o morcego está vivo, caso positivo o sistema verifica uma
        # segunda condição, se a velocidade for maior que zero muda para a imagem 1, senão usa a imagem 2
        if (morcego.alive):
            if (morcego.speed > 0):
                morcego.image = 'morcego1'
            else:
                morcego.image = 'morcego2'

        # Condição para atualizar os pontos
        if (estalactite1.right < morcego.left):
            morcego.score = estalactite1.number + estalactite2.number - 1

        if (estalactite2.right < morcego.left):
            morcego.score = estalactite1.number + estalactite2.number - 1

        # Condição para atualizar a pontuação máxima
        if (morcego.score > morcego.max_score):
            morcego.max_score = morcego.score

        # Condição para aumentar a velocidade do jogo
        if (morcego.score >= morcego.conta_ponto):
            morcego.velocidade_tela += 1
            morcego.conta_ponto += 10

# Desenha os objetos na tela
def draw():
    screen.blit('caverna', (0, 0))
    morcego.draw()
    estalactite1.draw()
    estalagmite1.draw()

    estalactite2.draw()
    estalagmite2.draw()

    # Desenha o quadro de pontos do jogador atual
    screen.draw.text(
        str(morcego.score),
        color = 'yellow',
        midtop = (WIDTH/2, 15),
        fontsize = 55
        )

    # Desenha o quadro de pontuação máxima da rodada
    screen.draw.text(
        str(morcego.max_score),
        color = 'green',
        midtop = (WIDTH - 50, 15),
        fontsize = 65
        )

# Executa sempre que o botão do mouse é pressionado
def on_mouse_down():
    if (morcego.started):
        if (morcego.alive):
            sounds.flap.play()
            morcego.speed = -6.5

# Função para reiniciar o jogo
def reset():
    morcego.speed = 1
    morcego.center = (75, 350)
    estalactite1.center = (250, 0)
    estalagmite1.center = (250, estalactite1.height + espaco)
    estalactite2.center = (720, 0)
    estalagmite2.center = (720, estalagmite2.height + espaco)
    morcego.alive = True
    morcego.image = 'morcego1'
    morcego.score = 0
    estalactite1.number = 1
    estalactite2.number = 1
    morcego.started = False
    morcego.velocidade_tela = 5
    morcego.conta_ponto = 10

# Função para executar os comandos depois da colisão
def colisao():
    morcego.image = "morcego-fantasma"
    morcego.alive = False

def on_key_down(key):
    #print(key)
    if (key == keys.SPACE):
        morcego.started = True

# Cria o personagem morcego do jogo
morcego = Actor('morcego1')

# Adicionando os obstáculos
#espaco = 180
espaco = 280
estalactite1 = Actor('estalactite1')
estalagmite1 = Actor('estalagmite1')
estalactite2 = Actor('estalactite2')
estalagmite2 = Actor('estalagmite2')

morcego.velocidade_tela = 5
morcego.conta_ponto = 10
gravidade = 0.3
morcego.max_score = 0

reset()