from PPlay.window import *
from PPlay.keyboard import *
from PPlay.sprite import *
from PPlay.animation import *
from settings import *
from game_objects.player import Player
from game_objects.bat import Bat
import random

class Game:
    def __init__(self, window):
        self.window = window
        self.keyboard = self.window.get_keyboard()
        
        self.player = Player()
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
        # Remove todos os morcegos mortos ou fora da tela
        self.bat_list = [bat for bat in self.bat_list if not bat.is_off_screen() and not bat.is_dead()]
                
    def draw_bats(self):
        for bat in self.bat_list:
            bat.draw()   
            
    def update(self, delta_time, keyboard):
        """Atualiza o estado do jogo"""
        self.player.update(delta_time, keyboard, self.bat_list)
        self.update_bats(delta_time)

    def draw(self):
        self.player.draw()
        self.draw_bats()
        self.window.draw_text(f"XP: {self.player.current_xp}", 0, 0, 15, 'white')
        self.window.draw_text(f"level: {self.player.level}", 0, 15, 15, 'white')
        dt = self.window.delta_time()
        fps = round(1/dt) if dt > 0 else 0
        self.window.draw_text(f"fps: {fps}", 0, 30, 15, 'white')

    def exit(self):
        if self.keyboard.key_pressed("ESC"):
            return True

    def run(self):
        self.window.set_background_color((44, 22, 62))
        self.update(self.window.delta_time(), self.keyboard)
        self.draw()
        self.exit()