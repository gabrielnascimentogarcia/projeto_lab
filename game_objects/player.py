# player.py (refatorado)
from PPlay.sprite import *
from PPlay.animation import *
from settings import *

class Player:
    """
    Classe que representa o jogador.
    Gerencia o movimento, ataque e sistema de XP/level.
    """
    def __init__(self, sound_manager):
        # Carregamento das animações
        self.player_idle = Sprite('imagens/player/player_idle.png', 7)
        self.player_idle.set_sequence_time(0, 7, PLAYER_IDLE_ANIMATION_DURATION, True)

        self.player_attacking = Sprite('imagens/player/player_attacking_down.png', 7)
        self.player_attacking.set_sequence_time(0, 7, PLAYER_ATTACK_ANIMATION_DURATION, False)
        
        # Gerenciador de som
        self.sound_manager = sound_manager
        
        # Posição inicial
        self.posXplayer = PLAYER_START_X
        self.posYplayer = 0
        
        # Estado do player
        self.player_state = 'idle'
        self.dash_active = False
        self.dash_target_y = 0 
        self.space_pressed = False
        self.shield_health = 2
        
        # Sistema de progressão
        self.current_xp = 0
        self.total_xp = 0  # XP acumulativo
        self.level = 1
        self.attribute_points = 0
        
        self.sword_strength = 0
        self.attack_speed_bonus = 0
        self.boot_speed_bonus = 0
        self.sword_range_bonus = 0
        self.shield_resistance_bonus = 0
        
    def _handle_idle_movement(self, delta_time, keyboard):
        # Movimento horizontal
        player_speed = PLAYER_SPEED * (1 + self.boot_speed_bonus * 0.1) * delta_time
        if keyboard.key_pressed('left'):
            self.posXplayer -= player_speed
        elif keyboard.key_pressed('right'):
            self.posXplayer += player_speed

        # Limita o movimento dentro da tela
        self.posXplayer = max(0, min(self.posXplayer, WIDTH - self.player_idle.width))

        # Inicia o dash se possível
        if keyboard.key_pressed('space'):
            if not self.space_pressed and not self.dash_active and self.posYplayer <= 0:
                self.player_state = 'attacking'
                self.player_attacking.play()
                self.sound_manager.play_sword_attack()
                self.dash_active = True
                self.dash_target_y = HEIGHT - self.player_attacking.height 
            self.space_pressed = True
        else:
            self.space_pressed = False

    def _handle_dash_movement(self, delta_time, bats):
        self._move_dash(delta_time)
        if self.player_state == 'attacking' and self.dash_active:
            self._check_dash_collisions(bats)
        if self.posYplayer >= self.dash_target_y and self.dash_active: 
            self._end_dash()

    def _move_dash(self, delta_time):
        """Move o player durante o dash"""
        if self.posYplayer < self.dash_target_y:
            dash_speed = PLAYER_DASH_SPEED * (1 + self.attack_speed_bonus * 0.2)
            self.posYplayer += dash_speed * delta_time
            if self.posYplayer > self.dash_target_y:
                self.posYplayer = self.dash_target_y

    def _check_dash_collisions(self, bats):
        """Verifica colisão do dash com os morcegos"""
        self.player_attacking.set_position(self.posXplayer, self.posYplayer)
        sword_width = 70 * (1 + self.sword_range_bonus * 0.3)
        sword_height = 20 * (1 + self.sword_range_bonus * 0.3)
        for bat in bats[:]:
            if self._process_bat_collision(bat, sword_width, sword_height):
                break

    def _process_bat_collision(self, bat, sword_width, sword_height):
        """Processa colisão e dano em um morcego durante o dash"""
        if bat.can_collide():
            bat_x = bat.fly_animation.x
            bat_y = bat.fly_animation.y
            if (abs(self.posXplayer - bat_x) < sword_width and 
                abs(self.posYplayer - bat_y) < sword_height):
                if self.player_attacking.collided_perfect(bat.fly_animation):
                    bat_died = bat.take_damage(self.sword_strength + 1)
                    if bat_died:
                        self.gain_xp(BAT_XP)
                    self._end_dash()
                    return True
        return False

    def _end_dash(self):
        """Finaliza o dash e reseta estado"""
        self.dash_active = False
        self.player_state = 'idle'
        self.player_attacking.stop()

    def _return_to_top(self, delta_time):
        """Retorna o player para o topo da tela após o dash"""
        if self.posYplayer > 0:
            self.posYplayer -= PLAYER_RETURN_SPEED * delta_time
            if self.posYplayer < 0:
                self.posYplayer = 0 
            
    def draw(self):
        """Renderiza o player"""
        self.player_idle.x = self.posXplayer
        self.player_idle.y = self.posYplayer
        self.player_attacking.x = self.posXplayer
        self.player_attacking.y = self.posYplayer
        
        if self.player_state == 'idle':
            self.player_idle.draw()
        elif self.player_state == 'attacking':
            self.player_attacking.draw()
            
    def gain_xp(self, amount):
        self.current_xp += amount
        self.total_xp += amount  

    def level_up(self):
        XP_TO_LEVEL_UP = XP_BASE * (FACTOR ** self.level - 1)
        self.current_xp -= XP_TO_LEVEL_UP
        self.level += 1
        self.attribute_points += 1

    def check_level_up(self):
        leveled_up = False
        XP_TO_LEVEL_UP = XP_BASE * (FACTOR ** self.level - 1)
        while self.current_xp >= XP_TO_LEVEL_UP:
            self.level_up()
            leveled_up = True
            XP_TO_LEVEL_UP = XP_BASE * (FACTOR ** self.level - 1)
        if leveled_up:
            self.sound_manager.play_player_levelup()
        return leveled_up
            
    def _update_animations(self):
        """Atualiza as animações do player"""
        if self.player_state == 'idle':
            self.player_idle.update()
        elif self.player_state == 'attacking':
            self.player_attacking.update()
            
    def update(self, delta_time, keyboard, bats):
        """Atualiza o estado do player"""
        bat_killed = False

        if self.player_state == 'idle':
            self._handle_idle_movement(delta_time, keyboard)
                
        if self.dash_active:
            bat_killed = self._handle_dash_movement(delta_time, bats)
            
        if self.player_state == 'idle' and self.posYplayer > 0:
            self._return_to_top(delta_time) 
        
        self._update_animations()

        return bat_killed