from random import randint

WIDTH = 700
HEIGHT = 394

alienigena = Actor('alien')

alienigena.topright = 0, randint(0, 300)

def draw():
    screen.blit('andromeda', (0, 0))
    alienigena.draw()

def update():
    alienigena.left += 2
    if alienigena.left > WIDTH:
        alienigena.right = 0
        muda_posicao_alien()

def on_mouse_down(pos):
    if alienigena.collidepoint(pos):
        acertou_alien()
    else:
        print('Errouuuuu!!!!')

def acertou_alien():
    sounds.ouch.play()
    alienigena.image = 'alien_hurt'
    clock.schedule_unique(voltar_alien_normal, 1.0)
    clock.schedule_unique(muda_posicao_alien, 1.0)

def voltar_alien_normal():
    alienigena.image = 'alien'

def muda_posicao_alien():
    alienigena.top = randint(0, 300)