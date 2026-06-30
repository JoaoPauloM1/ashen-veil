import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, SCENE_WIDTH, GROUND_Y, WORLD_WIDTH, PLAYER_MAX_ASHES
from entities.player import Player
from entities.dummy import Dummy
from worlds.cemetery import Cemetery
from transition import Transition
from interaction import InteractionSystem
from hud import HUD
from checkpoint import CheckpointSystem

pygame.init()

fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

cemetery = Cemetery()
player = Player(100, 300)
dummy = Dummy(SCENE_WIDTH + 400, GROUND_Y - 80)
transition = Transition()
interaction = InteractionSystem()
hud = HUD()
checkpoint = CheckpointSystem()

current_slot = 0

FREE_PASS_SLOTS = [1, 2, 3, 6, 7, 8]

FADE_RIGHT = {
    0: 1,
    3: 4,
    5: 6,
    8: 9,
    9: 10,
}

FADE_LEFT = {
    1: 0,
    4: 3,
    9: 8,
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
    player.rect.x = (prev_slot + 1) * SCENE_WIDTH - 200
    player.rect.y = GROUND_Y - player.rect.height

def respawn_player():
    # Chamado no meio do fade, quando a tela está completamente preta
    global current_slot

    # Volta para o slot do último checkpoint salvo
    current_slot = checkpoint.saved_slot

    # Reposiciona o jogador no início desse slot
    player.rect.x = current_slot * SCENE_WIDTH + 100
    player.rect.y = GROUND_Y - player.rect.height

    # Restaura Ashes e cargas de parry
    player.ashes = PLAYER_MAX_ASHES
    player.parry_charges = 0

    # Reseta o estado de morte
    player.is_dead = False

def check_scene_transitions():
    global current_slot

    if transition.active:
        return

    detected_slot = player.rect.centerx // SCENE_WIDTH
    detected_slot = max(0, min(detected_slot, 10))

    if detected_slot in FREE_PASS_SLOTS or detected_slot == current_slot:
        current_slot = detected_slot

    move_left, move_right = get_movement_bounds(current_slot)

    if player.rect.right >= move_right and current_slot in FADE_RIGHT:
        next_slot = FADE_RIGHT[current_slot]
        transition.start(lambda s=next_slot: change_scene(s))

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

    # Verifica morte ANTES das transições normais — tem prioridade
    if player.is_dead and not transition.active:
        transition.start(respawn_player)

    check_scene_transitions()
    transition.update()
    interaction.update(player.rect, cemetery.camera_x)
    checkpoint.check(current_slot)
    checkpoint.update()
    dummy.update()

    move_left, move_right = get_movement_bounds(current_slot)
    if player.rect.left < move_left:
        player.rect.left = move_left
    if player.rect.right > move_right:
        player.rect.right = move_right

    cam_left, cam_right = get_camera_bounds(current_slot)
    cemetery.update_camera(player.rect, cam_left, cam_right)

    player.update(GROUND_Y, [dummy])

    # ── DRAW ──
    screen.fill((0, 0, 0))
    cemetery.draw(screen)
    player.draw(screen, cemetery.camera_x)
    dummy.draw(screen, cemetery.camera_x)
    interaction.draw(screen)
    hud.draw(screen, player.ashes, player.parry_charges)
    checkpoint.draw(screen, player.rect, cemetery.camera_x)
    transition.draw(screen)
    pygame.display.flip()
    clock.tick(FPS)