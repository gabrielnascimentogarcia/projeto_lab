from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from PPlay.gameimage import *
from game_objects.player import Player
from game_objects.bat import Bat
from settings import *
import random

class Game:
    def __init__(self, window, sound_manager):
        self.window = window
        self.keyboard = self.window.get_keyboard()
        self.bg_image = GameImage("imagens/tela_game/fundo_jogo.png")
        self.sound_manager = sound_manager
        self.shield_quantity = []
        self.player = Player(sound_manager)
        self.bat_list = []
        self.spawn_timer = 0
        self.spawn_delay = MIN_SPAWN_DELAY
        self.game_over = False

    def update_health_ui(self):
        self.shield_quantity.clear()
        for i in range(self.player.shield_health):
            icon = GameImage("imagens/tela_atributos/icone_escudo.png")
            icon.set_position(0 + i * icon.width, 0)
            self.shield_quantity.append(icon)

    def draw_health_ui(self):
        for icon in self.shield_quantity:
            icon.draw()
            
    def spawn_bat(self):
        if len(self.bat_list) < MAX_BATS:
            x = random.randint(50, WIDTH - 50)
            bat = Bat(x, HEIGHT, self.player.level, self.sound_manager)
            self.bat_list.append(bat)
            
    def update_bats(self, delta_time):
        self.spawn_timer += delta_time
        level_factor = max(1, self.player.level * 0.7)
        adjusted_min_delay = MIN_SPAWN_DELAY / level_factor
        adjusted_max_delay = MAX_SPAWN_DELAY / level_factor

        if self.spawn_timer >= self.spawn_delay:
            self.spawn_bat()
            self.spawn_delay = adjusted_min_delay + (adjusted_max_delay - adjusted_min_delay) * (len(self.bat_list) / MAX_BATS)
            self.spawn_timer = 0

        for bat in self.bat_list[:]:
            bat.update(delta_time)
            
            if bat.is_off_screen() and not bat.is_dead():            
                self.player.shield_health -= 1
                if self.player.shield_health <= 0:
                    self.sound_manager.play_game_over()
                    self.game_over = True
                    self.sound_manager.stop_gameplay_music()  # Adicione esta linha
                else:
                    self.sound_manager.play_player_hurt()
                self.bat_list.remove(bat)
            
        self.bat_list = [bat for bat in self.bat_list if not bat.is_off_screen() and not bat.is_dead()]
                
    def draw_bats(self):
        for bat in self.bat_list:
            bat.draw()  
            
    def draw(self):
        self.bg_image.draw()
        self.player.draw()
        self.draw_bats() 
        self.draw_health_ui()
        
        #self.window.draw_text(f"XP: {self.player.current_xp}", 0, 0, 15, 'white')
        #self.window.draw_text(f"level: {self.player.level}", 0, 15, 15, 'white')
        #if self.window.delta_time() > 0:
            #fps = round(1/self.window.delta_time()) 
            #self.window.draw_text(f"fps: {fps}", 0, 45, 15, 'white')
            
        # Desenha a tela de game over
        if self.game_over:
            self._draw_game_over()

    def update(self, delta_time, keyboard):
        """Atualiza o estado do jogo"""
        if not self.game_over:
            self.player.update(delta_time, keyboard, self.bat_list)
            self.update_bats(delta_time)
            self.update_health_ui()
        
    def _draw_game_over(self):
        # Exibe a imagem de game over centralizada
        game_over_img = GameImage("imagens/tela_game/game_over.png")
        x = (WIDTH - game_over_img.width) // 2
        y = (HEIGHT - game_over_img.height) // 2
        game_over_img.set_position(x, y)
        game_over_img.draw()
        
    def exit(self):
        if self.keyboard.key_pressed("ESC"):
            return True
    
    def run(self):
        
        self.window.set_background_color((44, 22, 62))
        self.update(self.window.delta_time(), self.keyboard)
        self.draw()
        self.exit()