from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from settings import *

janela = Window(WIDTH, HEIGHT)
teclado = janela.get_keyboard()

player_idle = Sprite('imagens/player/player_idle.png', 7)
player_idle.set_sequence_time(0, 7, 400, True)

player_attacking = Sprite('imagens/player/player_attacking_down.png', 7)
player_attacking.set_sequence_time(0, 7, 50, False)

posXplayer = (WIDTH + player_idle.width)/3
posYplayer = 0
posYdash = HEIGHT - player_attacking.height

monster_list = []
monster = Sprite('imagens/monstro.png')
monster.set_position(WIDTH, 100)
monster_list.append(monster)

def movimento_player():
    player_idle.x = posXplayer
    player_idle.y = posYplayer
    player_attacking.x = posXplayer
    player_attacking.y = posYplayer
    
def desenho_player():
    global player_state
    
    if player_state == 'idle':
        player_idle.update()
        player_idle.draw()
    elif player_state == 'attacking':
        player_attacking.update()
        player_attacking.draw()

while True:        
    janela.set_background_color((44, 22, 62))

    if teclado.key_pressed('left'):
        posXplayer -= velXplayer * janela.delta_time()
    elif teclado.key_pressed('right'):
        posXplayer += velXplayer * janela.delta_time()

    if posXplayer < 0:
        posXplayer = 0
    if posXplayer > WIDTH - player_idle.width:
        posXplayer = WIDTH - player_idle.width
        
    if teclado.key_pressed('space') and player_state != 'attacking' and posYplayer <= 0:
        player_state = 'attacking'
        player_attacking.play()
    
    if player_state == 'attacking':   
        if posYplayer < posYdash:
            posYplayer += velYdash * janela.delta_time()
        if posYplayer > posYdash:
            posYplayer = posYdash    
            
        for monster in monster_list:
            if player_attacking.collided(monster):
                monster_list.remove(monster)
                player_state = 'idle'
                player_attacking.stop()
                break
                                
        if not player_attacking.is_playing():
            player_state = 'idle'
            player_attacking.stop()

    if player_state == 'idle' and posYplayer > 0:
        posYplayer -= 1000 * janela.delta_time()
        if posYplayer < 0:
            posYplayer = 0
    
    for monster in monster_list:
        monster.draw()
    
    movimento_player()
    desenho_player()

    janela.update()