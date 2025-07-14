from PPlay.animation import *
from settings import *
import math
import random # Adicionado: Importa o módulo random

class Bat:
    """
    Classe que representa um morcego inimigo.
    Gerencia o movimento, animações e estados do morcego.
    """
    def __init__(self, x, y, level, sound_manager):
        # Carregamento das animações
        self.fly_animation = Animation('imagens/Bat with VFX/fly.png', 8)
        self.fly_animation.set_sequence_time(0, 7, BAT_FLY_ANIMATION_DURATION, True)

        self.hurt_animation = Animation('imagens/Bat with VFX/hit.png', 8)
        self.hurt_animation.set_sequence_time(0, 7, BAT_HURT_ANIMATION_DURATION, False)

        self.die_animation = Animation('imagens/Bat with VFX/death.png', 8)
        self.die_animation.set_sequence_time(0, 7, BAT_DIE_ANIMATION_DURATION, False)

        # Gerenciador de som
        self.sound_manager = sound_manager

        # Posição inicial
        self.x = max(0, min(x, WIDTH - self.fly_animation.width))
        self.y = y
        self._update_animation_positions()

        # Estado do morcego
        self.current_level = level
        self.state = 'flying'
        self.hit_count = 0
        self.death_complete = False

        # Configurações de movimento ajustadas pelo nível do jogador
        self.horizontal_speed = BAT_SPEED * (1 + (self.current_level - 1) * 0.3) 
        self.vertical_speed = BAT_VERTICAL_SPEED * (1 + (self.current_level - 1) * 0.1) 
        self.direction = random.choice([-1, 1]) # Modificado: Inicia com direção aleatória

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

            # Movimento horizontal
            self.x += self.horizontal_speed * self.direction * delta_time

            # Limita o movimento dentro da tela e inverte direção ao atingir as bordas
            if self.x < 0:
                self.x = 0
                self.direction = 1
            elif self.x > WIDTH - self.fly_animation.width:
                self.x = WIDTH - self.fly_animation.width
                self.direction = -1

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

    def take_damage(self, damage):
        """Processa o dano recebido pelo morcego"""
        if self.state == 'flying':
            self.state = 'hurt'
            self.hurt_animation.play()
            self.sound_manager.play_bat_hurt()
            self.hit_count += damage
        if self.hit_count >= (BAT_HITS_TO_DIE + (self.current_level - 1) // 2):
            self.die()
            return True
        return False

    def die(self):
        """Inicia a animação de morte do morcego"""
        if self.state != 'dead' and not self.death_complete:
            self.state = 'dying'
            self.die_animation.play()
            self.sound_manager.play_bat_death()

    def is_dead(self):
        """Verifica se o morcego está morto"""
        return self.death_complete

    def is_off_screen(self):
        """Verifica se o morcego saiu da tela"""
        return self.y < -self.fly_animation.height

    def can_collide(self):
        """Verifica se o morcego pode colidir"""
        return self.state == 'flying' or self.state == 'hurt'