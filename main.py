import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, SCENE_WIDTH, GROUND_Y, WORLD_WIDTH
from entities.player import Player
from worlds.cemetery import Cemetery
from transition import Transition
from interaction import InteractionSystem

pygame.init()

fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

cemetery = Cemetery()
player = Player(100, 300)
transition = Transition()
interaction = InteractionSystem()

current_slot = 0

# Slots de passagem livre — jogador anda sem fade entre eles
FREE_PASS_SLOTS = [1, 2, 3, 6, 7, 8]

# Fade ao chegar no fim DIREITO do slot
FADE_RIGHT = {
    0: 1,
    3: 4,
    5: 6,
    8: 9,
    9: 10,
}

# Fade ao chegar no fim ESQUERDO do slot (voltar)
FADE_LEFT = {
    1: 0,   # início do loop cemiterio2 → volta para cemiterio1
    4: 3,   # cemiterio3 → volta para fim do loop cemiterio2
    9: 8,   # cemiterio6 → volta para fim do loop cemiterio5
    # slot 5 (interior igreja) — sem retorno
    # slot 10 (boss final) — sem retorno
}

def get_camera_bounds(slot):
    if slot in [1, 2, 3]:
        return 1 * SCENE_WIDTH, 4 * SCENE_WIDTH
    elif slot in [6, 7, 8]:
        return 6 * SCENE_WIDTH, 9 * SCENE_WIDTH
    else:
        return slot * SCENE_WIDTH, (slot + 1) * SCENE_WIDTH

def get_movement_bounds(slot):
    if slot in [1, 2, 3]:
        return 1 * SCENE_WIDTH, 4 * SCENE_WIDTH
    elif slot in [6, 7, 8]:
        return 6 * SCENE_WIDTH, 9 * SCENE_WIDTH
    else:
        return slot * SCENE_WIDTH, (slot + 1) * SCENE_WIDTH

def change_scene(next_slot):
    global current_slot
    current_slot = next_slot
    player.rect.x = next_slot * SCENE_WIDTH + 100
    player.rect.y = GROUND_Y - player.rect.height

def go_back(prev_slot):
    global current_slot
    current_slot = prev_slot
    # Posiciona o jogador no fim do slot anterior
    player.rect.x = (prev_slot + 1) * SCENE_WIDTH - 200
    player.rect.y = GROUND_Y - player.rect.height

def check_scene_transitions():
    global current_slot

    if transition.active:
        return

    # Atualiza o slot baseado na posição do jogador
    detected_slot = player.rect.centerx // SCENE_WIDTH
    detected_slot = max(0, min(detected_slot, 10))

    if detected_slot in FREE_PASS_SLOTS or detected_slot == current_slot:
        current_slot = detected_slot

    move_left, move_right = get_movement_bounds(current_slot)

    # Chegou no fim direito — fade para próximo slot
    if player.rect.right >= move_right and current_slot in FADE_RIGHT:
        next_slot = FADE_RIGHT[current_slot]
        transition.start(lambda s=next_slot: change_scene(s))

    # Chegou no fim esquerdo — fade para slot anterior
    elif player.rect.left <= move_left and current_slot in FADE_LEFT:
        prev_slot = FADE_LEFT[current_slot]
        transition.start(lambda s=prev_slot: go_back(s))

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                else:
                    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

            if event.key == pygame.K_f:
                name, zone = interaction.get_active_zone()
                if zone and not transition.active:
                    if name == "church_door":
                        transition.start(lambda: change_scene(5))
                    elif name == "well":
                        print("Entrando no poço — área subterrânea em breve!")
                    elif name == "final_gate":
                        print("Fim do Mundo 1!")

    # ── UPDATE ──
    check_scene_transitions()
    transition.update()
    interaction.update(player.rect, cemetery.camera_x)

    # Limites de movimento do jogador
    move_left, move_right = get_movement_bounds(current_slot)
    if player.rect.left < move_left:
        player.rect.left = move_left
    if player.rect.right > move_right:
        player.rect.right = move_right

    # Limites da câmera
    cam_left, cam_right = get_camera_bounds(current_slot)
    cemetery.update_camera(player.rect, cam_left, cam_right)

    player.update(GROUND_Y)

    # ── DRAW ──
    screen.fill((0, 0, 0))
    cemetery.draw(screen)
    player.draw(screen, cemetery.camera_x)
    interaction.draw(screen)
    transition.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)