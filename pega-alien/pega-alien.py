WIDTH = 700
HEIGHT = 394

alienigena = Actor('alien')
alienigena.pos = 100, 56

alienigena.topright = 10, 100

def draw():
    screen.blit('andromeda', (0, 0))
    alienigena.draw()

def update():
    alienigena.left += 2
    if alienigena.left > WIDTH:
        alienigena.right = 0

def on_mouse_down(pos):
    if alienigena.collidepoint(pos):
        acertou_alien()
    else:
        print('Errouuuuu!!!!')

def acertou_alien():
    sounds.ouch.play()
    alienigena.image
    alienigena.image = 'alien_hurt'
    clock.schedule_unique(voltar_alien_normal, 1.0)

def voltar_alien_normal():
    alienigena.image = 'alien'