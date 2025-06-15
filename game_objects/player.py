# player.py (refatorado)
from PPlay.sprite import *
from PPlay.animation import *
from settings import *
import math # Ainda necessário se você usar o Player para algo com math

class Player:
    def __init__(self):
        self.player_idle = Sprite('imagens/player/player_idle.png', 7)
        self.player_idle.set_sequence_time(0, 7, PLAYER_IDLE_ANIMATION_DURATION, True)

        self.player_attacking = Sprite('imagens/player/player_attacking_down.png', 7)
        self.player_attacking.set_sequence_time(0, 7, PLAYER_ATTACK_ANIMATION_DURATION, False)
        
        self.posXplayer = PLAYER_START_X
        self.posYplayer = 0
        
        self.player_state = 'idle'
        self.dash_active = False
        self.dash_target_y = 0 
        self.space_pressed = False
        
    def _handle_idle_movement(self, delta_time, keyboard):
        if keyboard.key_pressed('left'):
            self.posXplayer -= PLAYER_SPEED * delta_time
        elif keyboard.key_pressed('right'):
            self.posXplayer += PLAYER_SPEED * delta_time
            
        self.posXplayer = max(0, min(self.posXplayer, WIDTH - self.player_idle.width))
        
        if keyboard.key_pressed('space'):
            if not self.space_pressed and not self.dash_active and self.posYplayer <= 0:
                self.player_state = 'attacking'
                self.player_attacking.play()
                self.dash_active = True
                self.dash_target_y = HEIGHT - self.player_attacking.height 
            self.space_pressed = True
        else:
            self.space_pressed = False

    def _handle_dash_movement(self, delta_time, bats):
        bat_killed = False
        if self.posYplayer < self.dash_target_y:
            self.posYplayer += PLAYER_DASH_SPEED * delta_time
            if self.posYplayer > self.dash_target_y:
                self.posYplayer = self.dash_target_y
                
        for bat in bats[:]: 
            if bat.can_collide() and self.player_attacking.collided(bat.fly_animation):
                bat.take_damage()
                if bat.is_dead():
                    bat_killed = True 
                self.dash_active = False
                self.player_state = 'idle'
                self.player_attacking.stop()
                break 
                
        if self.posYplayer >= self.dash_target_y and self.dash_active: 
            self.dash_active = False
            self.player_state = 'idle'
            self.player_attacking.stop()
        return bat_killed
            
    def _return_to_top(self, delta_time):
        if self.posYplayer > 0:
            self.posYplayer -= PLAYER_RETURN_SPEED * delta_time
            if self.posYplayer < 0:
                self.posYplayer = 0 

    def _update_animations(self):
        if self.player_state == 'idle':
            self.player_idle.update()
        elif self.player_state == 'attacking':
            self.player_attacking.update()

    def update(self, delta_time, keyboard, bats):
        bat_killed = False

        if self.player_state == 'idle':
            self._handle_idle_movement(delta_time, keyboard)
                
        if self.dash_active:
            bat_killed = self._handle_dash_movement(delta_time, bats)
            
        if self.player_state == 'idle' and self.posYplayer > 0:
            self._return_to_top(delta_time) 
        
        self._update_animations()

        return bat_killed
            
    def draw(self):
        self.player_idle.x = self.posXplayer
        self.player_idle.y = self.posYplayer
        self.player_attacking.x = self.posXplayer
        self.player_attacking.y = self.posYplayer
        
        if self.player_state == 'idle':
            self.player_idle.draw()
        elif self.player_state == 'attacking':
            self.player_attacking.draw()