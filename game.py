from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from settings import *
import random
import math

class Bat:
    def __init__(self, x, y):
        # Carrega as animações
        self.fly_animation = Animation('imagens/Bat with VFX/Bat-IdleFly.png', 9)
        self.fly_animation.set_sequence_time(0, 8, BAT_FLY_ANIMATION_DURATION, True)
        
        self.hurt_animation = Animation('imagens/Bat with VFX/Bat-Hurt.png', 5)
        self.hurt_animation.set_sequence_time(0, 4, BAT_HURT_ANIMATION_DURATION, False)
        
        self.die_animation = Animation('imagens/Bat with VFX/Bat-Die.png', 12)
        self.die_animation.set_sequence_time(0, 11, BAT_DIE_ANIMATION_DURATION, False)
        
        # Define posição inicial
        self.x = max(0, min(x, WIDTH - self.fly_animation.width))
        self.y = y
        self.fly_animation.set_position(self.x, self.y)
        self.hurt_animation.set_position(self.x, self.y)
        self.die_animation.set_position(self.x, self.y)
        
        # Gerenciamento de estado
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
            # Movimento vertical
            self.y -= self.vertical_speed * delta_time
            
            # Movimento horizontal com oscilação
            horizontal_movement = math.sin(self.y * self.oscillation_frequency) * self.oscillation_speed * delta_time
            new_x = self.x + horizontal_movement
            
            # Verifica limites da tela
            if new_x < 0:
                new_x = 0
                self.oscillation_direction = 1
            elif new_x > WIDTH - self.fly_animation.width:
                new_x = WIDTH - self.fly_animation.width
                self.oscillation_direction = -1
                
            self.x = new_x
            
            # Atualiza posição das animações
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

class Game:
    def __init__(self):
        self.window = Window(WIDTH, HEIGHT)
        self.keyboard = self.window.get_keyboard()
        self.setup_player()
        self.setup_bats()
        
    def setup_player(self):
        # Configuração do player
        self.player_idle = Sprite('imagens/player/player_idle.png', 7)
        self.player_idle.set_sequence_time(0, 7, PLAYER_IDLE_ANIMATION_DURATION, True)
        
        self.player_attacking = Sprite('imagens/player/player_attacking_down.png', 7)
        self.player_attacking.set_sequence_time(0, 7, PLAYER_ATTACK_ANIMATION_DURATION, False)
        
        self.posXplayer = PLAYER_START_X
        self.posYplayer = 0
        self.posYdash = HEIGHT - self.player_attacking.height
        
        # Estado do player
        self.player_state = 'idle'
        self.dash_active = False
        self.dash_target_y = 0
        self.space_pressed = False
        
    def setup_bats(self):
        self.bat_list = []
        self.spawn_timer = 0
        self.spawn_delay = MIN_SPAWN_DELAY
        
    def spawn_bat(self):
        if len(self.bat_list) < MAX_BATS:
            x = random.randint(50, WIDTH - 50)
            bat = Bat(x, HEIGHT)
            self.bat_list.append(bat)
            
    def update_player(self, delta_time):
        if self.player_state == 'idle':
            # Movimento horizontal
            if self.keyboard.key_pressed('left'):
                self.posXplayer -= PLAYER_SPEED * delta_time
            elif self.keyboard.key_pressed('right'):
                self.posXplayer += PLAYER_SPEED * delta_time
                
            # Limites da tela
            self.posXplayer = max(0, min(self.posXplayer, WIDTH - self.player_idle.width))
            
            # Início do dash
            if self.keyboard.key_pressed('space'):
                if not self.space_pressed and not self.dash_active and self.posYplayer <= 0:
                    self.player_state = 'attacking'
                    self.player_attacking.play()
                    self.dash_active = True
                    self.dash_target_y = self.posYdash
                self.space_pressed = True
            else:
                self.space_pressed = False
                
        # Movimento do dash
        if self.dash_active:
            if self.posYplayer < self.dash_target_y:
                self.posYplayer += PLAYER_DASH_SPEED * delta_time
                if self.posYplayer > self.dash_target_y:
                    self.posYplayer = self.dash_target_y
                    
            # Verifica colisões durante o dash
            for bat in self.bat_list[:]:
                if bat.can_collide() and self.player_attacking.collided(bat.fly_animation):
                    bat.take_damage()
                    if bat.is_dead():
                        self.bat_list.remove(bat)
                    self.dash_active = False
                    self.player_state = 'idle'
                    self.player_attacking.stop()
                    break
                    
            # Finaliza o dash
            if self.posYplayer >= self.dash_target_y:
                self.dash_active = False
                self.player_state = 'idle'
                self.player_attacking.stop()
                
        # Retorno ao topo
        if self.player_state == 'idle' and self.posYplayer > 0:
            self.posYplayer -= PLAYER_RETURN_SPEED * delta_time
            if self.posYplayer < 0:
                self.posYplayer = 0
                
    def update_bats(self, delta_time):
        # Atualiza spawn de morcegos
        self.spawn_timer += delta_time
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_bat()
            self.spawn_delay = MIN_SPAWN_DELAY + (MAX_SPAWN_DELAY - MIN_SPAWN_DELAY) * (len(self.bat_list) / MAX_BATS)
            self.spawn_timer = 0
            
        # Atualiza e desenha morcegos
        for bat in self.bat_list[:]:
            bat.update(delta_time)
            bat.draw()
            if bat.is_off_screen() or bat.is_dead():
                self.bat_list.remove(bat)
                
    def draw_player(self):
        self.player_idle.x = self.posXplayer
        self.player_idle.y = self.posYplayer
        self.player_attacking.x = self.posXplayer
        self.player_attacking.y = self.posYplayer
        
        if self.player_state == 'idle':
            self.player_idle.update()
            self.player_idle.draw()
        elif self.player_state == 'attacking':
            self.player_attacking.update()
            self.player_attacking.draw()
            
    def run(self):
        while True:
            self.window.set_background_color((44, 22, 62))
            delta_time = self.window.delta_time()
            
            self.update_player(delta_time)
            self.update_bats(delta_time)
            self.draw_player()
            
            self.window.update()

if __name__ == "__main__":
    game = Game()
    game.run()