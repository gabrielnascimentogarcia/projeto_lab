from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

# Configurações da janela
WIDTH, HEIGHT = 600, 900
window = Window(WIDTH, HEIGHT)
window.set_title("Atributos do Personagem")

# Imagens (agora reais)
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

# Posições do painel
painel_x = (WIDTH - painel.width) // 2
painel_y = (HEIGHT - painel.height) // 2

# Layout dos atributos
atributos = [
    ("Força da Espada", 0),
    ("Velocidade de Ataque", 1),
    ("Velocidade das Botas", 2),
    ("Alcance da Espada", 3),
    ("Resistência do Escudo", 4)
]

# Cálculo de espaçamento vertical dinâmico
num_atributos = len(atributos)
espaco_top = 60  # margem superior dentro do painel
espaco_bottom = 120  # espaço para o botão confirmar
altura_util = painel.height - espaco_top - espaco_bottom
linha_espaco = altura_util // num_atributos

# Posições horizontais relativas ao painel
icone_offset_x = 32
texto_offset_x = icone_offset_x + icones[0].width + 24
valor_offset_x = painel.width - botao_mais.width - 64 - 40  # 40px para valor
botao_offset_x = painel.width - botao_mais.width - 32

# Botão confirmar centralizado na base do painel
confirmar_x = painel_x + (painel.width - botao_confirmar.width) // 2
confirmar_y = painel_y + painel.height - botao_confirmar.height - 32

mouse = window.get_mouse()

# Valores dos atributos
valores = [0 for _ in atributos]

# Controle de clique para evitar múltiplos incrementos por clique
mouse_was_pressed = False

running = True
while running:
    fundo.set_position(0, 0)
    fundo.draw()
    painel.set_position(painel_x, painel_y)
    painel.draw()

    # Desenhar cada atributo
    for i, (nome, idx) in enumerate(atributos):
        y = painel_y + espaco_top + i * linha_espaco
        icon = icones[idx]
        # Ícone
        icon.set_position(painel_x + icone_offset_x, y + (linha_espaco - icon.height)//2)
        icon.draw()
        # Nome
        window.draw_text(
            nome,
            painel_x + texto_offset_x,
            y + (linha_espaco - 16)//2,  # 16 = tamanho da fonte
            size=16, color=(255,255,255), font_name="Arial", bold=True
        )
        # Valor do atributo
        window.draw_text(
            str(valores[i]),
            painel_x + valor_offset_x,
            y + (linha_espaco - 28)//2,
            size=28, color=(255,255,255), font_name="Arial", bold=True
        )
        # Botão +
        bx = painel_x + botao_offset_x
        by = y + (linha_espaco - botao_mais.height)//2
        botao_mais.set_position(bx, by)
        botao_mais.draw()

        # Detectar clique no botão +
        mouse_x, mouse_y = mouse.get_position()
        mouse_over_mais = bx <= mouse_x <= bx + botao_mais.width and by <= mouse_y <= by + botao_mais.height
        if mouse.is_button_pressed(1) and mouse_over_mais and not mouse_was_pressed:
            valores[i] += 1
            mouse_was_pressed = True

    # Botão confirmar
    botao_confirmar.set_position(confirmar_x, confirmar_y)
    botao_confirmar.draw()

    window.update()

    # Navegação: sair com ENTER ou clique no confirmar
    keyboard = window.get_keyboard()
    mouse_x, mouse_y = mouse.get_position()
    mouse_click_confirmar = mouse.is_button_pressed(1) and \
        confirmar_x <= mouse_x <= confirmar_x + botao_confirmar.width and \
        confirmar_y <= mouse_y <= confirmar_y + botao_confirmar.height
    if keyboard.key_pressed("ENTER") or mouse_click_confirmar:
        running = False

    # Reset do controle de clique
    if not mouse.is_button_pressed(1):
        mouse_was_pressed = False

window.close() 