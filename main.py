from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from PPlay.keyboard import Keyboard
from game import Game
from settings import WIDTH, HEIGHT

class GameManager:
    """
    Gerenciador principal do jogo.
    Controla os estados do jogo e a transição entre menu e gameplay.
    """
    def __init__(self):
        # Inicialização da janela e controles
        self.window = Window(WIDTH, HEIGHT)
        self.window.set_title("Epic Sky Boss Battle")
        self.mouse = self.window.get_mouse()
        self.keyboard = self.window.get_keyboard()
        
        # Carregamento dos assets do menu
        self._load_menu_assets()
        
        # Estado inicial do jogo
        self.current_state = "menu"
        self.game = None
        
    def _load_menu_assets(self):
        """Carrega e posiciona os elementos do menu principal"""
        # Carregamento das imagens
        self.bg_image = GameImage("imagens/fundo_menu.png")
        self.logo_image = GameImage("imagens/logo.png")
        self.botao_iniciar = GameImage("imagens/botao_iniciar.png")
        
        # Cálculo das posições
        self.logo_x = (WIDTH - self.logo_image.width) // 2
        self.logo_y = 80
        self.botao_x = (WIDTH - self.botao_iniciar.width) // 2
        self.botao_y = HEIGHT - 400
        
    def run_menu(self):
        """Renderiza e atualiza o menu principal"""
        # Desenho dos elementos do menu
        self.bg_image.set_position(0, 0)
        self.bg_image.draw()

        self.logo_image.set_position(self.logo_x, self.logo_y)
        self.logo_image.draw()

        self.botao_iniciar.set_position(self.botao_x, self.botao_y)
        self.botao_iniciar.draw()

        # Créditos
        self.window.draw_text(
            "Gabriel França & Gabriel Garcia",
            WIDTH // 2 - 160, HEIGHT - 60,
            size=20, color=(180, 180, 180), font_name="Arial", italic=True
        )

        # Verificação de input para iniciar o jogo
        if self._check_menu_input():
            self.current_state = "game"
            self.game = Game(self.window)
            
    def _check_menu_input(self):
        """Verifica se o jogador quer iniciar o jogo"""
        mouse_click = self.mouse.is_button_pressed(1) and \
            self.botao_x <= self.mouse.get_position()[0] <= self.botao_x + self.botao_iniciar.width and \
            self.botao_y <= self.mouse.get_position()[1] <= self.botao_y + self.botao_iniciar.height
            
        return self.keyboard.key_pressed("ENTER") or mouse_click
            
    def run_game(self):
        """Atualiza e renderiza o estado do jogo"""

        # Verificação de retorno ao menu
        if self.keyboard.key_pressed("ESC"):
            self.current_state = "menu"
            self.game = None
            return
        
        if self.game is None:
            return
        
        # Atualização do estado do jogo
        self.window.set_background_color((44, 22, 62))
        delta_time = self.window.delta_time()
        
        # Atualização do player e verificação de colisões
        bat_killed = self.game.player.update(delta_time, self.keyboard, self.game.bat_list)
        if bat_killed:
            self.game.bat_list = [bat for bat in self.game.bat_list if not bat.is_dead()]
        
        # Atualização dos morcegos
        self.game.update_bats(delta_time)
        
        # Renderização
        self.game.player.draw() 
        self.game.draw_bats() 

        # Interface do jogador
        self._draw_hud()
        
    def _draw_hud(self):
        if self.game is None:
            return
        
        """Renderiza a interface do jogador"""
        self.window.draw_text(f"XP: {self.game.player.current_xp}", 0, 0, 15, 'white')
        self.window.draw_text(f"level: {self.game.player.level}", 0, 15, 15, 'white')
        
    def run(self):
        """Loop principal do jogo"""
        while True:
            if self.current_state == "menu":
                self.run_menu()
            else:
                self.run_game()
                
            self.window.update()

if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run() 