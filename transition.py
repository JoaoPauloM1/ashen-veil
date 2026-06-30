import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT

class Transition:
    def __init__(self):
        # Superfície preta que cobre a tela para o fade
        self.surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.surface.fill((0, 0, 0))

        self.alpha = 0           # 0 = transparente, 255 = preto total
        self.speed = 5           # velocidade do fade
        self.fading_out = False  # True = escurecendo, False = clareando
        self.active = False      # se uma transição está acontecendo
        self.done = False        # sinaliza que o fade terminou e pode trocar de cena
        self.callback = None     # função a chamar no meio da transição

    def start(self, callback):
        # Inicia uma transição — callback é o que acontece no meio (trocar de cena)
        self.active = True
        self.fading_out = True
        self.done = False
        self.alpha = 0
        self.callback = callback

    def update(self):
        if not self.active:
            return

        if self.fading_out:
            # Fase 1 — escurece a tela
            self.alpha += self.speed
            if self.alpha >= 255:
                self.alpha = 255
                self.fading_out = False
                # Chama o callback no momento mais escuro
                if self.callback:
                    self.callback()
        else:
            # Fase 2 — clareia a tela
            self.alpha -= self.speed
            if self.alpha <= 0:
                self.alpha = 0
                self.active = False
                self.done = True

    def draw(self, screen):
        if self.active or self.alpha > 0:
            self.surface.set_alpha(self.alpha)
            screen.blit(self.surface, (0, 0))