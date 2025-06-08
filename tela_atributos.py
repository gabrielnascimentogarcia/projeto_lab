from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse
from PPlay.keyboard import Keyboard # Importação explícita é uma boa prática

# --- Configurações Iniciais (sem alterações) ---
WIDTH, HEIGHT = 600, 900
window = Window(WIDTH, HEIGHT)
window.set_title("Atributos do Personagem")
fundo = GameImage("imagens/fundo_atributos.png")
painel = GameImage("imagens/painel_atributos.png")
icones = [
    GameImage("imagens/icone_forca.png"),
    GameImage("imagens/icone_ataque.png"),
    GameImage("imagens/icone_botas.png"),
    GameImage("imagens/icone_espada_alcance.png"),
    GameImage("imagens/icone_escudo.png")
]
botao_mais = GameImage("imagens/botao_mais.png")
botao_confirmar = GameImage("imagens/botao_confirmar.png")
painel_x = (WIDTH - painel.width) // 2
painel_y = (HEIGHT - painel.height) // 2
atributos = [
    ("Força da Espada", 0),
    ("Velocidade de Ataque", 1),
    ("Velocidade das Botas", 2),
    ("Alcance da Espada", 3),
    ("Resistência do Escudo", 4)
]
num_atributos = len(atributos)
espaco_top = 60
espaco_bottom = 120
altura_util = painel.height - espaco_top - espaco_bottom
linha_espaco = altura_util // num_atributos
icone_offset_x = 32
texto_offset_x = icone_offset_x + icones[0].width + 24
valor_offset_x = painel.width - botao_mais.width - 64 - 40
botao_offset_x = painel.width - botao_mais.width - 32
confirmar_x = painel_x + (painel.width - botao_confirmar.width) // 2
confirmar_y = painel_y + painel.height - botao_confirmar.height - 32

# --- Variáveis e Objetos (com otimizações) ---
mouse = window.get_mouse()
keyboard = window.get_keyboard() # <--- MOVIDO para fora do loop

valores = [0 for _ in atributos]
mouse_was_pressed = False

# Define a posição de imagens estáticas uma única vez
fundo.set_position(0, 0)
painel.set_position(painel_x, painel_y)
botao_confirmar.set_position(confirmar_x, confirmar_y) # <--- MOVIDO para fora do loop

running = True
while running:
    # --- OTIMIZAÇÃO: Obter posição do mouse uma vez por quadro ---
    mouse_x, mouse_y = mouse.get_position()
    is_mouse_clicking = mouse.is_button_pressed(1) # <--- OTIMIZAÇÃO: checar o clique uma vez

    # --- Desenho ---
    fundo.draw()
    painel.draw()
    botao_confirmar.draw() # Desenha o botão confirmar (posição já foi definida)

    # Desenhar cada atributo
    for i, (nome, idx) in enumerate(atributos):
        y = painel_y + espaco_top + i * linha_espaco
        icon = icones[idx]
        
        icon.set_position(painel_x + icone_offset_x, y + (linha_espaco - icon.height)//2)
        icon.draw()
        
        window.draw_text(nome, painel_x + texto_offset_x, y + (linha_espaco - 16)//2, size=16, color=(255,255,255), font_name="Arial", bold=True)
        window.draw_text(str(valores[i]), painel_x + valor_offset_x, y + (linha_espaco - 28)//2, size=28, color=(255,255,255), font_name="Arial", bold=True)
        
        bx = painel_x + botao_offset_x
        by = y + (linha_espaco - botao_mais.height)//2
        botao_mais.set_position(bx, by)
        botao_mais.draw()

        # Detectar clique no botão +
        mouse_over_mais = bx <= mouse_x <= bx + botao_mais.width and by <= mouse_y <= by + botao_mais.height
        if is_mouse_clicking and mouse_over_mais and not mouse_was_pressed:
            valores[i] += 1
            mouse_was_pressed = True

    # --- Navegação: sair com ENTER ou clique no confirmar ---
    mouse_over_confirmar = confirmar_x <= mouse_x <= confirmar_x + botao_confirmar.width and confirmar_y <= mouse_y <= confirmar_y + botao_confirmar.height
    
    # LÓGICA CORRIGIDA: Usa a flag `mouse_was_pressed` para o botão confirmar também
    if is_mouse_clicking and mouse_over_confirmar and not mouse_was_pressed:
        running = False
        # mouse_was_pressed = True # Opcional, já que vamos sair do loop
        
    if keyboard.key_pressed("ENTER"):
        running = False

    # Reset do controle de clique
    if not is_mouse_clicking:
        mouse_was_pressed = False
        
    window.update()

window.close()