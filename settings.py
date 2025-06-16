# Configurações da Janela
WIDTH, HEIGHT = 600, 900

# Configurações do Player
PLAYER_SPEED = 300          # Velocidade de movimento horizontal
PLAYER_DASH_SPEED = 2000    # Velocidade do dash
PLAYER_RETURN_SPEED = 3000  # Velocidade de retorno após o dash
PLAYER_START_X = WIDTH // 3 # Posição inicial X do player

# Sistema de XP e Level
XP_BASE = 100              # XP base necessária para o primeiro level
FACTOR = 1.5               # Fator de multiplicação do XP para próximos levels
BAT_XP = 10.0              # XP ganho por morcego morto

# Configurações dos Morcegos
BAT_SPEED = 150            # Velocidade horizontal
BAT_VERTICAL_SPEED = 150   # Velocidade vertical
BAT_OSCILLATION_SPEED = 50 # Velocidade da oscilação
BAT_OSCILLATION_FREQUENCY = 0.01  # Frequência da oscilação
BAT_HITS_TO_DIE = 1        # Número de hits para matar um morcego
MAX_BATS = 8               # Número máximo de morcegos na tela
MIN_SPAWN_DELAY = 1.0      # Delay mínimo entre spawns
MAX_SPAWN_DELAY = 2.0      # Delay máximo entre spawns

# Configurações de Animação (duração em milissegundos)
BAT_FLY_ANIMATION_DURATION = 50
BAT_HURT_ANIMATION_DURATION = 50
BAT_DIE_ANIMATION_DURATION = 50
PLAYER_IDLE_ANIMATION_DURATION = 400
PLAYER_ATTACK_ANIMATION_DURATION = 100