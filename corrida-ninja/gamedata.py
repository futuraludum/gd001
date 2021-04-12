"""
Definições de todos os objetos do jogo
"""

from pgzero.actor import Actor

TITLE = 'Corrida Ninja'
WIDTH = 1024  # Largura da área de jogo.
HEIGHT = 384  # Altura da área de jogo.
DISTANCE = 200  # Distância para vencer.
LEVEL_UP = 100  # Número de passos antes de aumentar a dificuldade.
speed = 20  # Velocidade de movimento dos objetos (não ninja).
object_frequency = 100  # Frequência de aparecimento dos objetos (quando menor mais frequente).
powerup_frequency = 400  # Frequência de aparecimento do power up.
steps = 0  # Contador de frames do jogo.
PULL = 2  # Custo dos passos quando chutar.
PUSH = 2  # Benefício em voar.
FALL = 10  # Custo de bater em alguma coisa.
FLIGHT_TIME = 2  # Tempo de voo em segundos.
STARTED = False  # Corrida iniciada?
END = False  # Corrida finalizada?
WARNING = False  # Exibição da informação de distância.

ground_objects = {
    'small_ground': {
        'pos': [320, 320],
        'items': [
            'cat',
            'dog',
            'box',
            'fire_hydrant',
            'traffic_cone',
            'undergrowth',
        ],
    },
    'large_ground': {
        'pos': [312, 312],
        'items': [
            'barrels',
            'barrier',
            'bushes',
            'fence',
            'motorbike',
        ],
    },
}

air_objects = {
    'small_air': {
        'pos': [48, 280],
        'items': [
            'kite',
            'star',
        ],
    },
    'large_air': {
        'pos': [64, 240],
        'items': [
            'balloon',
            'comet',
            'cloud',
            'jet',
            'satellite',
        ],
    },
}

active_objects = []  # Non-player objects to avoid.
power_up = None  # Represents am antigravity power-up in the game world.


red = Actor('red_run1')  # Represents "Red"
red.name = 'red'  # Used to select which colour animation to use.
red.pos = (512, 304)  # Start position
red.frame = 1  # Start frame for the animations.
red.jumping = False  # Jumping state.
red.flying = False  # Flying state.
red.kicking = False  # Kicking state.
red.landing = False  # Landing state.
red.hit = False  # Hit non-player object state.
red.antigravity = 0  # The number of "flights" red can make.

blue = Actor('blue_run1')  # Represents "Blue"
blue.name = 'blue'  # Used to select which colour animation to use.
blue.pos = (512, 304)  # Start position.
blue.frame = 3  # Start frame for the animation.
blue.jumping = False  # Jumping state.
blue.flying = False  # Flying state.
blue.kicking = False  # Kicking state.
blue.landing = False  # Landing state.
blue.hit = False  # Hit non-player object state.
blue.antigravity = 0  # The number of "flights" blue can make.

# Floors are drawn one after the other for smooth scrolling.
floor_a = Actor('floor')
floor_a.pos = 0, 332
floor_b = Actor('floor')
floor_b.pos = 1024, 332