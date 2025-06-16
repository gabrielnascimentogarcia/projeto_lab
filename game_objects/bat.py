from PPlay.animation import *
from settings import *
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