from PPlay.window import Window
from game import Game
from main_menu import MainMenu
from attributes_screen import AttributesScreen
from sound_manager import SoundManager
from settings import WIDTH, HEIGHT

class GameManager:
    def __init__(self):
        # Inicialização da janela e controles
        self.window = Window(WIDTH, HEIGHT)
        self.window.set_title("Epic Sky Boss Battle")
        self.mouse = self.window.get_mouse()
        self.keyboard = self.window.get_keyboard()
        
        # Inicialização do gerenciador de som
        self.sound_manager = SoundManager()
        
        self.game = Game(self.window, self.sound_manager)
        self.main_menu = MainMenu(self.window, self.sound_manager)        
        self.attributes_screen = AttributesScreen(self.window, self.game.player, self.sound_manager)
        self.current_state = "main_menu"
            
    def change_current_state(self):
        if self.current_state == "main_menu":
            if self.main_menu.button_clicked():
                self.current_state = "gameplay" 
                self.sound_manager.play_gameplay_music()
                
        elif self.current_state == "gameplay":
            if self.game.player.check_level_up():
                self.attributes_screen.points_to_spend = self.game.player.attribute_points
                self.current_state = "attributes_screen"
            if self.game.exit():
                self._reset_game()
                self.current_state = "main_menu"
                self.sound_manager.play_menu_music()
                
        elif self.current_state == "attributes_screen":
            if self.attributes_screen._handle_confirmar():
                self.current_state = "gameplay"
                
    def _reset_game(self):
        """Reseta o jogo para o estado inicial"""
        self.game = Game(self.window, self.sound_manager)
        self.attributes_screen = AttributesScreen(self.window, self.game.player, self.sound_manager)
                
    def run(self):
        # Inicia com a música do menu
        self.sound_manager.play_menu_music()
        
        while True:
            self.change_current_state()
            if self.current_state == "main_menu":
                self.main_menu.run()
            elif self.current_state == "gameplay":
                self.game.run()
            if self.current_state == "attributes_screen":
                self.attributes_screen.run()
            self.window.update()

