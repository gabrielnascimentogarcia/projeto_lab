from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *

posXplayer = 300
posYplayer = 0
velXplayer = 300
velYplayer = 300
player_state = 'idle'
is_attacking = False
start_attack_timer = 0
attack_duration_ms = 50

WIDTH, HEIGHT = 600, 900
janela = Window(WIDTH, HEIGHT)
teclado = janela.get_keyboard()

player_idle = Sprite('imagens/player/player_idle.png', 7)
player_idle.set_sequence_time(0, 7, 400, True)

player_walking = Sprite('imagens/player/player_walking.png', 8)
player_walking.set_sequence_time(0, 8, 100, True)

player_attacking = Sprite('imagens/player/player_attacking.png', 14)
player_attacking.set_sequence_time(0, 14, attack_duration_ms, False)

def movimento_player():
    player_idle.x = posXplayer
    player_idle.y = posYplayer
    player_walking.x = posXplayer
    player_walking.y = posYplayer
    player_attacking.x = posXplayer
    player_attacking.y = posYplayer
    
def desenho_player():
    global is_attacking, player_state
    
    if player_state == 'idle':
        player_idle.update()
        player_idle.draw()
    elif player_state == 'walking':
        player_walking.update()
        player_walking.draw()
    elif player_state == 'attacking':
        player_attacking.update()
        player_attacking.draw()

while True:        
    janela.set_background_color('white')
    
    if player_state == 'walking':
        player_state = 'idle'
    
    if teclado.key_pressed('left'):
        if player_state != 'attacking': player_state = 'walking'
        posXplayer -= velXplayer * janela.delta_time()
    elif teclado.key_pressed('right'):
        if player_state != 'attacking': player_state = 'walking'
        posXplayer += velXplayer * janela.delta_time()
    if teclado.key_pressed('up'):
        if player_state != 'attacking': player_state = 'walking'
        posYplayer -= velYplayer * janela.delta_time()
    elif teclado.key_pressed('down'):
        if player_state != 'attacking': player_state = 'walking'
        posYplayer += velYplayer * janela.delta_time()    

    running_time = janela.time_elapsed()
    if teclado.key_pressed('space') and running_time - start_attack_timer > 500:
        player_state = 'attacking'
        player_attacking.play()
        start_attack_timer = running_time
            
    if player_state == 'attacking':
        if running_time - start_attack_timer > 500:
            player_state = 'idle'
            player_attacking.stop()

    movimento_player()
    desenho_player()

    janela.update()