import pygame

# ─── TELA ────────────────────────────────────────────────────
SCREEN_WIDTH  = 1280
SCREEN_HEIGHT = 720
FPS           = 60
TITLE         = "Ashen Veil"

# ─── MUNDO ───────────────────────────────────────────────────
SCENE_WIDTH  = SCREEN_WIDTH
SCENE_HEIGHT = SCREEN_HEIGHT
NUM_SCENES   = 11                    # total de slots no mundo
WORLD_WIDTH  = SCREEN_WIDTH * NUM_SCENES

# ─── CHÃO ────────────────────────────────────────────────────
GROUND_Y = 545    # 80% de 720px — mesmo chão para todos os cenários

# ─── VAEL (PLAYER) ───────────────────────────────────────────
PLAYER_SPEED        = 4
PLAYER_JUMP_FORCE   = -12
GRAVITY             = 0.5
PLAYER_MAX_ASHES    = 2
PLAYER_WIDTH        = 40
PLAYER_HEIGHT       = 70

# ─── COMBATE ─────────────────────────────────────────────────
PARRY_WINDOW_MS        = 300    # Tempo em ms que a janela de parry fica aberta
DUMMY_ATTACK_COOLDOWN  = 2500   # Tempo entre ataques do dummy (ms)
DUMMY_TELEGRAPH_MS     = 800    # Tempo de aviso antes do ataque (ms)
PARRY_RANGE            = 150    # Distância máxima para o parry funcionar