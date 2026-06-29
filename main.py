import pygame
import sys
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE
from entities.player import Player

pygame.init()

fullscreen = False
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# Cria o Vael no centro inferior da tela
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 200)

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

    # ── UPDATE ──
    player.update()  # Atualiza toda a lógica do Vael

    # ── DRAW ──
    screen.fill((0, 0, 0))
    player.draw(screen)  # Desenha o Vael na tela
    pygame.display.flip()
    clock.tick(FPS)