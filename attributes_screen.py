from PPlay.window import *
from PPlay.gameimage import *
from PPlay.mouse import *
from PPlay.keyboard import *
from settings import *
from PPlay.sprite import *

class AttributesScreen:
    def __init__(self, window):
        self.window = window
        self.fundo = GameImage("imagens/tela_atributos/fundo_atributos.png")
        self.painel = GameImage("imagens/tela_atributos/painel_atributos.png")
        self.icones = [
            Sprite("imagens/tela_atributos/icone_forca.png"),
            Sprite("imagens/tela_atributos/icone_ataque.png"),
            Sprite("imagens/tela_atributos/icone_botas.png"),
            Sprite("imagens/tela_atributos/icone_espada_alcance.png"),
            Sprite("imagens/tela_atributos/icone_escudo.png")
        ]
        self.botao_mais = Sprite("imagens/tela_atributos/botao_mais.png")
        self.botao_confirmar = Sprite("imagens/tela_atributos/botao_confirmar.png")
        self.painel_x = (WIDTH - self.painel.width) // 2
        self.painel_y = (HEIGHT - self.painel.height) // 2
        self.atributos = [
            ("Força da Espada", 0),
            ("Velocidade de Ataque", 1),
            ("Velocidade das Botas", 2),
            ("Alcance da Espada", 3),
            ("Resistência do Escudo", 4)
        ]
        self.num_atributos = len(self.atributos)
        self.espaco_top = 60
        self.espaco_bottom = 120
        self.altura_util = self.painel.height - self.espaco_top - self.espaco_bottom
        self.linha_espaco = self.altura_util // self.num_atributos
        self.icone_offset_x = 32
        self.texto_offset_x = self.icone_offset_x + self.icones[0].width + 24
        self.valor_offset_x = self.painel.width - self.botao_mais.width - 64 - 40
        self.botao_offset_x = self.painel.width - self.botao_mais.width - 32
        self.confirmar_x = self.painel_x + (self.painel.width - self.botao_confirmar.width) // 2
        self.confirmar_y = self.painel_y + self.painel.height - self.botao_confirmar.height - 32

        self.keyboard = self.window.get_keyboard()
        self.mouse = self.window.get_mouse()
        self.valores = [0 for _ in self.atributos]
        self.mouse_was_pressed = False

        self.fundo.set_position(0, 0)
        self.painel.set_position(self.painel_x, self.painel_y)
        self.botao_confirmar.set_position(self.confirmar_x, self.confirmar_y)

    def _draw_base(self):
        self.fundo.draw()
        self.painel.draw()
        self.botao_confirmar.draw()

    def _draw_atributos(self, mouse_x, mouse_y, is_mouse_clicking):
        for i, (nome, idx) in enumerate(self.atributos):
            y = self.painel_y + self.espaco_top + i * self.linha_espaco
            icon = self.icones[idx]
            icon.set_position(self.painel_x + self.icone_offset_x, y + (self.linha_espaco - icon.height)//2)
            icon.draw()
            self.window.draw_text(nome, self.painel_x + self.texto_offset_x, y + (self.linha_espaco - 16)//2, size=16, color=(255,255,255), font_name="Arial", bold=True)
            self.window.draw_text(str(self.valores[i]), self.painel_x + self.valor_offset_x, y + (self.linha_espaco - 28)//2, size=28, color=(255,255,255), font_name="Arial", bold=True)
            self._handle_botao_mais(i, y, mouse_x, mouse_y, is_mouse_clicking)

    def _handle_botao_mais(self, i, y, mouse_x, mouse_y, is_mouse_clicking):
        bx = self.painel_x + self.botao_offset_x
        by = y + (self.linha_espaco - self.botao_mais.height)//2
        self.botao_mais.set_position(bx, by)
        self.botao_mais.draw()
        mouse_over_mais = bx <= mouse_x <= bx + self.botao_mais.width and by <= mouse_y <= by + self.botao_mais.height
        if is_mouse_clicking and mouse_over_mais and not self.mouse_was_pressed:
            self.valores[i] += 1
            self.mouse_was_pressed = True

    def _handle_confirmar(self):
        if self.mouse.is_over_object(self.botao_confirmar) and self.mouse.is_button_pressed(1):
            return True
        
    def _reset_mouse(self, is_mouse_clicking):
        if not is_mouse_clicking:
            self.mouse_was_pressed = False
            
    def run(self):
        mouse_x, mouse_y = self.mouse.get_position()
        is_mouse_clicking = self.mouse.is_button_pressed(1)

        self._draw_base()
        self._draw_atributos(mouse_x, mouse_y, is_mouse_clicking)
        self._handle_confirmar()
        self._reset_mouse(is_mouse_clicking)