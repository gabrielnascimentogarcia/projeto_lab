from PPlay.animation import *
from settings import *
import math

class Bat:
    """
    Classe que representa um morcego inimigo.
    Gerencia o movimento, animações e estados do morcego.
    """
    def __init__(self, x, y):
        # Carregamento das animações
        self.fly_animation = Animation('imagens/Bat with VFX/fly.png', 8)
        self.fly_animation.set_sequence_time(0, 7, BAT_FLY_ANIMATION_DURATION, True)
        
        self.hurt_animation = Animation('imagens/Bat with VFX/hit.png', 8)
        self.hurt_animation.set_sequence_time(0, 7, BAT_HURT_ANIMATION_DURATION, False)
        
        self.die_animation = Animation('imagens/Bat with VFX/death.png', 8)
        self.die_animation.set_sequence_time(0, 7, BAT_DIE_ANIMATION_DURATION, False)
        
        # Posição inicial
        self.x = max(0, min(x, WIDTH - self.fly_animation.width))
        self.y = y
        self._update_animation_positions()
        
        # Estado do morcego
        self.state = 'flying'
        self.speed = BAT_SPEED
        self.vertical_speed = BAT_VERTICAL_SPEED
        self.hit_count = 0
        self.death_complete = False
        
        # Configurações de movimento
        self.oscillation_direction = 1
        self.oscillation_speed = BAT_OSCILLATION_SPEED
        self.oscillation_frequency = BAT_OSCILLATION_FREQUENCY
        
    def _update_animation_positions(self):
        """Atualiza a posição de todas as animações"""
        self.fly_animation.set_position(self.x, self.y)
        self.hurt_animation.set_position(self.x, self.y)
        self.die_animation.set_position(self.x, self.y)
        
    def update(self, delta_time):
        """Atualiza o estado do morcego"""
        if self.state == 'flying':
            # Movimento vertical
            self.y -= self.vertical_speed * delta_time
            
            # Movimento horizontal oscilante
            horizontal_movement = math.sin(self.y * self.oscillation_frequency) * self.oscillation_speed * delta_time
            new_x = self.x + horizontal_movement
            
            # Limita o movimento dentro da tela
            if new_x < 0:
                new_x = 0
                self.oscillation_direction = 1
            elif new_x > WIDTH - self.fly_animation.width:
                new_x = WIDTH - self.fly_animation.width
                self.oscillation_direction = -1
                
            self.x = new_x
            self._update_animation_positions()
            self.fly_animation.update()
            
        elif self.state == 'hurt':
            self.hurt_animation.update()
            if not self.hurt_animation.is_playing():
                self.state = 'flying'
                self.hurt_animation.stop()
                
        elif self.state == 'dying':
            self.die_animation.update()
            if not self.die_animation.is_playing() and not self.death_complete:
                self.state = 'dead'
                self.death_complete = True
                self.die_animation.stop()
                
    def draw(self):
        """Renderiza o morcego baseado em seu estado"""
        if self.state == 'flying':
            self.fly_animation.draw()
        elif self.state == 'hurt':
            self.hurt_animation.draw()
        elif self.state == 'dying':
            self.die_animation.draw()
            
    def take_damage(self):
        """Processa o dano recebido pelo morcego"""
        if self.state == 'flying':
            self.state = 'hurt'
            self.hurt_animation.play()
            self.hit_count += 1
            if self.hit_count >= BAT_HITS_TO_DIE:
                self.die()
                return True
        return False
            
    def die(self):
        """Inicia a animação de morte do morcego"""
        if self.state != 'dead' and not self.death_complete:
            self.state = 'dying'
            self.die_animation.play()
            
    def is_dead(self):
        """Verifica se o morcego está morto"""
        return self.death_complete
        
    def is_off_screen(self):
        """Verifica se o morcego saiu da tela"""
        return self.y < -self.fly_animation.height
        
    def can_collide(self):
        """Verifica se o morcego pode colidir"""
        return self.state == 'flying' or self.state == 'hurt'