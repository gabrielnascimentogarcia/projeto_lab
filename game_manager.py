from PPlay.window import Window
from game import Game
from menu import MainMenu
from tela_atributos import TelaAtributos
from settings import WIDTH, HEIGHT

class GameManager:
    def __init__(self):
        # Inicialização da janela e controles
        self.window = Window(WIDTH, HEIGHT)
        self.window.set_title("Epic Sky Boss Battle")
        self.mouse = self.window.get_mouse()
        self.keyboard = self.window.get_keyboard()
        self.game = Game(self.window)
        self.main_menu = MainMenu(self.window)        
        self.tela_atributos = TelaAtributos(self.window)
        self.current_state = "main_menu"
            
    def change_current_state(self):
        if self.current_state == "main_menu":
            if self.main_menu.button_clicked():
                self.current_state = "gameplay" 
        elif self.current_state == "gameplay":
            if self.game.exit():
                self.current_state = "main_menu"
            
    def run(self):
        while True:
            self.change_current_state()
            if self.current_state == "main_menu":
                self.main_menu.run()
            if self.current_state == "gameplay":
                self.game.run()
            self.window.update()
