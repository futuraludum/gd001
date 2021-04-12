import random
#Importa as definições do jogo (arquivo gamedata.py)
from gamedata import *

music.play('running_music')

def update_player(player):
    """
    Atualizar a imagem do jogador de acordo com a ação.
    """
    if player.jumping:
        player.image = "{}_run3".format(player.name)
    elif player.kicking:
        player.image = "{}_kick".format(player.name)
        player.left -= PULL
    else:
        if player.flying:
            player.left += PUSH
            player.image = "{}_fly{}".format(player.name, player.frame)
        else:
            player.image = "{}_run{}".format(player.name, player.frame)
        player.frame += 1
        if player.frame > 5:
            player.frame = 1

def animate_update():
    """
    Atualiza as imagens.
    """
    global steps
    global speed
    global object_frequency
    global active_objects
    global power_up
    global END

    # Aumenta a dificuldade.
    steps += 1
    if steps % LEVEL_UP == 0:
        speed = min(40, speed + 4)  # Objetos se movem mais rapidamente.
        # Objetos aparecem com mais frequência.
        object_frequency = max(50, object_frequency - 5)
    # Atualiza imagens dos jogadores.
    update_player(red)
    update_player(blue)
    # Faz o chão se movimentar (rolar) continuamente.
    floor_a.left -= speed
    floor_b.left -= speed
    if int(floor_a.right) < 0:
        floor_a.left = floor_b.right
    if int(floor_b.right) < 0:
        floor_b.left = floor_a.right
    # Movimenta objetos.
    for obj in active_objects:
        obj.left -= speed
    # Movimenta o power-up
    if power_up:
        power_up.left -= speed
        if power_up.right < 0:
            power_up = None
    # Checa a condição de vitória
    distance_between_players = abs(red.left - blue.left)
    if (distance_between_players > DISTANCE or red.right < 0 or
            blue.right < 0):
        END = True
    else:
        # Redefine a chamada para esta função (que acontece a cada 8 milissegundos).
        clock.schedule_unique(animate_update, 0.08)

def toggle_warning():
    """
    Usado para exibir a distância em passos.
    """
    global WARNING
    WARNING = not WARNING
    clock.schedule_unique(toggle_warning, 0.5)

def jump(player, on_finished):
    if not player.flying:
        player.jumping = True
        x, y = player.pos
        animate(player, pos=(x, 204), duration=0.5,
                on_finished=on_finished, tween='decelerate')

def fall(player, on_finished):
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.3,
            on_finished=on_finished, tween='accelerate')

def fly_up(player):
    if not player.landing:
        x, y = player.pos
        animate(player, pos=(x, max(20, y - 50)),
                duration=0.1, tween='accelerate')

def fly_down(player, on_land):
    if not player.landing:
        x, y = player.pos
        new_y = y + 50
        if new_y < 290:
            animate(player, pos=(x, new_y), duration=0.1,
                    tween='accelerate')
        else:
            on_land()

def kick(player, on_land):
    player.kicking = True
    clock.schedule_unique(on_land, 0.6)

def land(player, on_land):
    player.landing = True
    x, y = player.pos
    animate(player, pos=(x, 304), duration=0.1, tween='accelerate',
            on_finished=on_land)

def red_land():
    land(red, red_reset)

def red_reset():
    red.jumping = False
    red.flying = False
    red.kicking = False
    red.landing = False

def red_jump():
    jump(red, red_fall)

def red_fall():
    fall(red, red_reset)

def blue_land():
    land(blue, blue_reset)

def blue_jump():
    jump(blue, blue_fall)

def blue_fall():
    fall(blue, blue_reset)

def blue_reset():
    blue.jumping = False
    blue.flying = False
    blue.kicking = False
    blue.landing = False

def update():
    """
    Atualiza o estado do jogo.
    """
    if END:
        update_end()
    elif STARTED:
        update_race()
    else:
        update_intro()

def update_intro():
    """
    Aguarda a barra de espaço ser pressionada para iniciar.
    """
    global STARTED
    if keyboard[keys.SPACE]:
        STARTED = True
        # Start the race.
        clock.schedule_unique(animate_update, 0.08)

def update_end():
    """
    Aguarda a barra de espaço ser pressionada para reiniciar.
    """
    global STARTED
    global END
    global speed
    global object_frequency
    global steps
    global active_objects
    if keyboard[keys.SPACE]:
        STARTED = True
        END = False
        speed = 20  # Velocidade dos objetos (não jogador).
        object_frequency = 100  # Menor = mais frequente.
        steps = 0
        red.pos = (512, 304)
        blue.pos = (512, 304)
        red.flying = False
        blue.flying = False
        red.jumping = False
        blue.jumping = False
        red.antigravity = 0
        blue.antigravity = 0
        active_objects = []
        # Inicia a corrida.
        clock.schedule_unique(animate_update, 0.08)

def update_race():
    """
    Atualiza o estado do jogo enquando os jogadores correm.
    """
    global active_objects
    global power_up

    # Vermelho
    if keyboard[keys.RETURN] and not red.jumping:
        red_jump()
    if keyboard[keys.UP] and not red.jumping:
        if red.antigravity > 0 and not red.flying:
            red.antigravity -= 1
            red.flying = True
            clock.schedule_unique(red_land, FLIGHT_TIME)
        if red.flying:
            fly_up(red)
    if keyboard[keys.DOWN]:
        fly_down(red, red_land)
    if (keyboard[keys.RIGHT] and not red.kicking and
            not red.flying):
        kick(red, red_reset)

    # Azul
    if keyboard[keys.LSHIFT] and not blue.jumping:
        blue_jump()
    if keyboard[keys.W] and not blue.jumping:
        if blue.antigravity > 0 and not blue.flying:
            blue.antigravity -= 1
            blue.flying = True
            clock.schedule_unique(blue_land, FLIGHT_TIME)
        if blue.flying:
            fly_up(blue)
    if keyboard[keys.S]:
        fly_down(blue, blue_land)
    if (keyboard[keys.D] and not blue.kicking and
            not blue.flying):
        kick(blue, blue_reset)

    # Checa as colisões entre os jogadores e objetos.
    for obj in active_objects:
        # Passou pelo objeto.
        if obj.right < 0:
            active_objects.remove(obj)
        # Objeto foi chutado.
        if obj.left > 1999:
            active_objects.remove(obj)
        # Colisão do vermelho.
        if red.colliderect(obj) and not obj.red_hit:
            if red.kicking:
                x = random.randint(2000, 4000)
                y = random.randint(0, HEIGHT)
                animate(obj, pos=(x, y), duration=0.2, tween='accelerate')
            else:
                red.left -= FALL
                obj.red_hit = True
                if red.flying:
                    red_land()
        # Colisão do azul.
        if blue.colliderect(obj) and not obj.blue_hit:
            if blue.kicking:
                x = random.randint(2000, 4000)
                y = random.randint(0, HEIGHT)
                animate(obj, pos=(x, y), duration=0.2, tween='accelerate')
            else:
                blue.left -= FALL
                obj.blue_hit = True
                if blue.flying:
                    blue_land()
    # Colisão com power-up.
    if power_up:
        # Faz um balanceamento caso os dois jogadores cheguem juntos ao power-up.
        touching_red = (red.colliderect(power_up) and not (red.flying or red.kicking)
                        and red.antigravity < 3)
        touching_blue = (blue.colliderect(power_up) and not (blue.flying or blue.kicking)
                         and blue.antigravity < 3)
        if touching_blue and touching_red:
            if red.antigravity > blue.antigravity:
                blue.antigravity += 1
            elif red.antigravity < blue.antigravity:
                red.antigravity += 1
            else:
                if random.choice([True, False]):
                    red.antigravity += 1
                else:
                    blue.antigravity += 1
            power_up = None
        elif touching_red:
            red.antigravity += 1
            power_up = None
        elif touching_blue:
            blue.antigravity += 1
            power_up = None
    if random.randint(0, object_frequency) == 0 or not active_objects:
        make_obstacle(ground_objects)
    if random.randint(0, object_frequency) == 0 or not active_objects:
        make_obstacle(air_objects)
    if not power_up and random.randint(0, powerup_frequency) == 0:
        power_up = Actor('antigravity', pos=(1024, 320))

def make_obstacle(objects):
    global active_objects
    obj_collection = objects[random.choice(list(objects.keys()))]
    low = obj_collection['pos'][0]
    high = obj_collection['pos'][1]
    new_object = Actor(random.choice(obj_collection['items']),
                       pos=(1024, random.randint(low, high)))
    new_object.red_hit = False
    new_object.blue_hit = False
    active_objects.append(new_object)

def draw():
    """
    Draw things on the screen.
    """
    screen.blit('paper', (0, 0))
    if END:  # A corrida encerrou.
        draw_end()
    elif STARTED:  # A corrida iniciou.
        draw_race()
    else:  # Mostra a tela inicial.
        draw_intro()

def draw_intro():
    """
    Desenha a tela inicial do jogo com a história e os comandos.
    """
    # Paper
    screen.draw.text('Corrida', (240, 10),
                     fontname='funsized', fontsize=56,
                     color=(0, 0, 255), background='None')
    # Chase
    screen.draw.text('Ninja', (550, 10),
                     fontname='funsized', fontsize=56,
                     color=(255, 0, 0), background='None')
    # Story
    story = ("A disputa entre dois grupos ninja (vermelho e azul) "
             "acontece tem muitos eras, as guerras entre elas deixaram "
             "um grande estrago no mundo.\nMas os chefes encontram uma maneira de resolver esta encrenca : "
             "a CORRIDA NINJA...").format(DISTANCE)
    screen.draw.text(story, (50, 100), width=900,
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 0))
    screen.draw.text('W - voar, S - descer\nD - chutar, Shift (esquerda) - pular.', (50, 240),
                     fontname='rudiment', fontsize=30,
                     color=(0, 0, 255))
    screen.draw.text('Seta acima - voar, Seta abaixo - descer\nSeta direita - chutar, Enter - pular.', (500, 240),
                     fontname='rudiment', fontsize=30,
                     color=(255, 0, 0))
    screen.draw.text('Pressione ESPACO para iniciar a corrida.', (240, 320),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0), background='None')

def draw_end():
    """
    Desenha o encerramento do jogo com o resultado final.
    """
    winner = 'Vermelho' if red.left > blue.left else 'Azul'
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    screen.draw.text('{} venceu!'.format(winner), (250, 100),
                     fontname='funsized', fontsize=56,
                     color=color, background='None')
    screen.draw.text('Pressione ESPACO to reiniciar.', (300, 250),
                     fontname='rudiment', fontsize=38,
                     color=(0, 0, 0), background='None')

def draw_race():
    """
    Exibe o estado do jogo enquanto os ninjas estão correndo.
    """
    red.draw()
    blue.draw()
    floor_a.draw()
    floor_b.draw()
    for obj in active_objects:
        obj.draw()
    if power_up:
        power_up.draw()
    screen.draw.text('Voar: {}'.format(red.antigravity),
                     (800, 340), fontname='rudiment', fontsize=38,
                     color=(255, 0, 0), background='None')
    screen.draw.text('Voar: {}'.format(blue.antigravity),
                     (580, 340), fontname='rudiment', fontsize=38,
                     color=(0, 0, 255), background='None')
    distance_between_players = int(abs(red.left - blue.left))
    distance_to_display = distance_between_players - (distance_between_players % 10)
    color = (255, 0, 0) if red.left > blue.left else (0, 0, 255)
    alert_margin = int((DISTANCE / 4) * 3)
    if distance_to_display < alert_margin:
        screen.draw.text('Passos na frente: {}'.format(distance_to_display),
                         (10, 340), fontname='rudiment', fontsize=38,
                         color=color, background='None')
    elif WARNING:
        screen.draw.text('Passos na frente: {}'.format(distance_to_display),
                         (10, 340), fontname='rudiment', fontsize=38,
                         color=color, background='None')

toggle_warning()