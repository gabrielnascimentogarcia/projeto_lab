from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from settings import *
from PPlay.gameimage import *

janela = Window(WIDTH, HEIGHT)
teclado = janela.get_keyboard()
bg_image = GameImage("imagens/fundo_menu.png")
bg_image.set_position(0, 0)

player_idle = Sprite('imagens/player/player_idle.png', 7)
player_idle.set_sequence_time(0, 7, 400, True)

player_attacking = Sprite('imagens/player/player_attacking_down.png', 7)
player_attacking.set_sequence_time(0, 7, 50, False)

posXplayer = (WIDTH + player_idle.width)/3
posYplayer = 0
posYdash = HEIGHT - player_attacking.height

monster_list = []
monster = Sprite('imagens/monstro.png')
monster.set_position(WIDTH/2, 500)
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
    
    bg_image.draw()

    if xp_counter != 0 and xp_counter % 100 == 0:
        xp_counter = 0
        player_level += 1
        attribute_points += 1
        
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
                if 1 <= player_level <= 5:
                    xp_counter += 10
                elif 5 < player_level <= 9: 
                    xp_counter += 5
                elif player_level == 10:
                    xp_counter = 0
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
        
        
    janela.draw_text(f"XP: {int(xp_counter)}", 0, 0, size=50, color=('white'), font_name='Comic Sans')
    janela.draw_text(f"level: {int(player_level-1)}", 0, 30, size=50, color=('white'), font_name='Comic Sans')
    janela.draw_text(f"attribute_points: {int(attribute_points)}", 0, 60, size=50, color=('white'), font_name='Comic Sans')
     
    if teclado.key_pressed('esc'):            
        monster = Sprite('imagens/monstro.png')
        monster.set_position(WIDTH/2, 500)
        monster_list.append(monster)
            
    movimento_player()
    desenho_player()

    janela.update()