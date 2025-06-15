from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from settings import *
import random
import math

class Bat:
    def __init__(self, x, y):
        self.fly_animation = Animation('imagens/Bat with VFX/Bat-IdleFly.png', 9)
        self.fly_animation.set_sequence_time(0, 8, BAT_FLY_ANIMATION_DURATION, True)
        
        self.hurt_animation = Animation('imagens/Bat with VFX/Bat-Hurt.png', 5)
        self.hurt_animation.set_sequence_time(0, 4, BAT_HURT_ANIMATION_DURATION, False)
        
        self.die_animation = Animation('imagens/Bat with VFX/Bat-Die.png', 12)
        self.die_animation.set_sequence_time(0, 11, BAT_DIE_ANIMATION_DURATION, False)
        
        self.x = max(0, min(x, WIDTH - self.fly_animation.width))
        self.y = y
        self.fly_animation.set_position(self.x, self.y)
        self.hurt_animation.set_position(self.x, self.y)
        self.die_animation.set_position(self.x, self.y)
        
        self.state = 'flying'
        self.speed = BAT_SPEED
        self.vertical_speed = BAT_VERTICAL_SPEED
        self.hit_count = 0
        self.death_complete = False
        self.oscillation_direction = 1
        self.oscillation_speed = BAT_OSCILLATION_SPEED
        self.oscillation_frequency = BAT_OSCILLATION_FREQUENCY
        
    def update(self, delta_time):
        if self.state == 'flying':
            self.y -= self.vertical_speed * delta_time
            
            horizontal_movement = math.sin(self.y * self.oscillation_frequency) * self.oscillation_speed * delta_time
            new_x = self.x + horizontal_movement
            
            if new_x < 0:
                new_x = 0
                self.oscillation_direction = 1
            elif new_x > WIDTH - self.fly_animation.width:
                new_x = WIDTH - self.fly_animation.width
                self.oscillation_direction = -1
                
            self.x = new_x
            
            self.fly_animation.set_position(self.x, self.y)
            self.hurt_animation.set_position(self.x, self.y)
            self.die_animation.set_position(self.x, self.y)
            self.fly_animation.update()
            
        elif self.state == 'hurt':
            self.hurt_animation.update()
            if not self.hurt_animation.is_playing():
                self.state = 'flying'
                
        elif self.state == 'dying':
            self.die_animation.update()
            if not self.die_animation.is_playing() and not self.death_complete:
                self.state = 'dead'
                self.death_complete = True
                
    def draw(self):
        if self.state == 'flying':
            self.fly_animation.draw()
        elif self.state == 'hurt':
            self.hurt_animation.draw()
        elif self.state == 'dying':
            self.die_animation.draw()
            
    def take_damage(self):
        if self.state == 'flying':
            self.state = 'hurt'
            self.hurt_animation.play()
            self.hit_count += 1
            if self.hit_count >= BAT_HITS_TO_DIE:
                self.die()
            
    def die(self):
        if self.state != 'dead' and not self.death_complete:
            self.state = 'dying'
            self.die_animation.play()
            
    def is_dead(self):
        return self.death_complete
        
    def is_off_screen(self):
        return self.y < -self.fly_animation.height
        
    def can_collide(self):
        return self.state == 'flying' or self.state == 'hurt'

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
        self.dash_target_y = 0 # Isso será definido pelo Game
        self.space_pressed = False
        
    def update(self, delta_time, keyboard, bats):
        # Retorna True se um morcego foi abatido, False caso contrário
        bat_killed = False

        if self.player_state == 'idle':
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
                    self.dash_target_y = HEIGHT - self.player_attacking.height # Target de dash
                self.space_pressed = True
            else:
                self.space_pressed = False
                
        if self.dash_active:
            if self.posYplayer < self.dash_target_y:
                self.posYplayer += PLAYER_DASH_SPEED * delta_time
                if self.posYplayer > self.dash_target_y:
                    self.posYplayer = self.dash_target_y
                    
            for bat in bats[:]: # Itera sobre uma cópia para evitar problemas ao remover
                if bat.can_collide() and self.player_attacking.collided(bat.fly_animation):
                    bat.take_damage()
                    if bat.is_dead():
                        bat_killed = True # Sinaliza que um morcego foi abatido
                    self.dash_active = False
                    self.player_state = 'idle'
                    self.player_attacking.stop()
                    break # Colidiu com um morcego, encerra o loop
                    
            if self.posYplayer >= self.dash_target_y and self.dash_active: # Verifica dash_active para evitar reset precoce
                self.dash_active = False
                self.player_state = 'idle'
                self.player_attacking.stop()
            
        if self.player_state == 'idle' and self.posYplayer > 0:
            self.posYplayer -= PLAYER_RETURN_SPEED * delta_time
            if self.posYplayer < 0:
                self.posYplayer = 0 
        
        # Atualiza as animações
        if self.player_state == 'idle':
            self.player_idle.update()
        elif self.player_state == 'attacking':
            self.player_attacking.update()

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

class Game:
    def __init__(self):
        self.window = Window(WIDTH, HEIGHT)
        self.keyboard = self.window.get_keyboard()
        
        self.player = Player() # Instancia o player e o armazena
        self.bat_list = []
        self.spawn_timer = 0
        self.spawn_delay = MIN_SPAWN_DELAY
        
    def spawn_bat(self):
        if len(self.bat_list) < MAX_BATS:
            x = random.randint(50, WIDTH - 50)
            bat = Bat(x, HEIGHT)
            self.bat_list.append(bat)
                
    def update_bats(self, delta_time):
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_bat()
            self.spawn_delay = MIN_SPAWN_DELAY + (MAX_SPAWN_DELAY - MIN_SPAWN_DELAY) * (len(self.bat_list) / MAX_BATS)
            self.spawn_timer = 0
            
        for bat in self.bat_list[:]:
            bat.update(delta_time)
            if bat.is_off_screen() or bat.is_dead():
                self.bat_list.remove(bat)
                
    def draw_bats(self):
        for bat in self.bat_list:
            bat.draw()
            
    def run(self):
        while True:
            self.window.set_background_color((44, 22, 62))
            delta_time = self.window.delta_time()
            
            bat_killed = self.player.update(delta_time, self.keyboard, self.bat_list)
            if bat_killed:
                self.bat_list = [bat for bat in self.bat_list if not bat.is_dead()]
            
            self.update_bats(delta_time)
            
            self.player.draw() 
            self.draw_bats() 

            self.window.update()

if __name__ == "__main__":
    game = Game()
    game.run()