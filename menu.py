from PPlay.gameimage import *
from PPlay.window import *
from PPlay.mouse import *
from PPlay.sprite import *
from settings import *

class MainMenu:
    def __init__(self, window) -> None:
        self.window = window
        self.mouse = window.get_mouse()
        self.bg_image = GameImage("imagens/fundo_menu.png")
        self.logo_image = GameImage("imagens/logo.png")
        self.botao_iniciar = Sprite("imagens/botao_iniciar.png")
        
        self.logo_x = (WIDTH - self.logo_image.width) // 2
        self.logo_y = 80
        self.botao_x = (WIDTH - self.botao_iniciar.width) // 2
        self.botao_y = HEIGHT - 400
        
        self.bg_image.set_position(0, 0)
        self.logo_image.set_position(self.logo_x, self.logo_y)
        self.botao_iniciar.set_position(self.botao_x, self.botao_y)

    def draw(self):
        self.bg_image.draw()
        self.logo_image.draw()
        self.botao_iniciar.draw()
        self.window.draw_text(
            "Gabriel França & Gabriel Garcia",
            WIDTH // 2 - 160, HEIGHT - 60,
            size=20, color=(180, 180, 180), font_name="Arial", italic=True
        )
        
    def button_clicked(self):
        if self.mouse.is_over_object(self.botao_iniciar) and self.mouse.is_button_pressed(1):
            return True
        
    def run(self):
        self.draw()
        self.button_clicked()
        
        
        
