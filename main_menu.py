from PPlay.window import Window
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

# Configurações da janela
WIDTH, HEIGHT = 600, 900
window = Window(WIDTH, HEIGHT)
window.set_title("Epic Sky Boss Battle")

# Imagens
bg_image = GameImage("imagens/fundo_menu.png")
logo_image = GameImage("imagens/logo.png")
botao_iniciar = GameImage("imagens/botao_iniciar.png")

# Posições
logo_x = (WIDTH - logo_image.width) // 2
logo_y = 80
botao_x = (WIDTH - botao_iniciar.width) // 2
botao_y = HEIGHT - 400

mouse = window.get_mouse()

# Loop da tela inicial
running = True
while running:
    bg_image.set_position(0, 0)
    bg_image.draw()

    logo_image.set_position(logo_x, logo_y)
    logo_image.draw()

    botao_iniciar.set_position(botao_x, botao_y)
    botao_iniciar.draw()

    # Instruções extras
    window.draw_text(
        "Gabriel França & Gabriel Garcia",
        WIDTH // 2 - 160, HEIGHT - 60,
        size=20, color=(180, 180, 180), font_name="Arial", italic=True
    )

    window.update()

    # Verifica clique no botão ou ENTER
    keyboard = window.get_keyboard()
    mouse_click = mouse.is_button_pressed(1) and \
        botao_x <= mouse.get_position()[0] <= botao_x + botao_iniciar.width and \
        botao_y <= mouse.get_position()[1] <= botao_y + botao_iniciar.height
    if keyboard.key_pressed("ENTER") or mouse_click:
        running = False

window.close() 