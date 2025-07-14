from PPlay.gameimage import *
from PPlay.window import *
from PPlay.mouse import *
from PPlay.sprite import *
from settings import *

class MainMenu:
    def __init__(self, window, sound_manager) -> None:
        self.window = window
        self.mouse = window.get_mouse()
        self.sound_manager = sound_manager
        self.bg_image = GameImage("imagens/tela_inicial/fundo_menu.png")
        self.logo_image = GameImage("imagens/tela_inicial/logo.png")
        self.botao_iniciar = Sprite("imagens/tela_inicial/botao_iniciar.png")
        logo_x = (WIDTH - self.logo_image.width) // 2
        logo_y = 80
        botao_x = (WIDTH - self.botao_iniciar.width) // 2
        botao_y = HEIGHT - 400
        self.bg_image.set_position(0, 0)
        self.logo_image.set_position(logo_x, logo_y)
        self.botao_iniciar.set_position(botao_x, botao_y)
        self._was_hovering = False

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
        hovering = self.mouse.is_over_object(self.botao_iniciar)
        if hovering and not self._was_hovering:
            self.sound_manager.play_botao_hover()
        self._was_hovering = hovering
        if hovering and self.mouse.is_button_pressed(1):
            self.sound_manager.play_botao_click()
            return True
        
    def run(self):
        self.draw()
        self.button_clicked()
        
        
        
