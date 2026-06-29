import pygame
from settings import (
    PLAYER_SPEED,
    PLAYER_JUMP_FORCE,
    GRAVITY,
    PLAYER_MAX_ASHES,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT
)

class Player(pygame.sprite.Sprite):
    # pygame.sprite.Sprite é uma classe base do Pygame que nos dá
    # funcionalidades prontas como detecção de colisão

    def __init__(self, x, y):
        # __init__ é o método construtor — roda automaticamente
        # quando criamos um Vael. x e y são a posição inicial dele
        super().__init__()  # Inicializa a classe pai (Sprite)

        # ── APARÊNCIA (temporária, sem arte ainda) ──
        # Cria um retângulo cinza representando o Vael por enquanto
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill((180, 180, 180))  # Cinza, cor das cinzas

        # rect é o retângulo que define posição e tamanho do Vael
        # é por ele que o Pygame sabe onde desenhar e detectar colisão
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # ── MOVIMENTO ──
        self.speed = PLAYER_SPEED
        self.velocity_y = 0      # Velocidade vertical (afetada pela gravidade)
        self.on_ground = False   # Controla se o Vael está no chão ou no ar

        # ── SISTEMA DE ASHES ──
        self.ashes = PLAYER_MAX_ASHES  # Começa com 2 Ashes

        # ── SISTEMA DE PARRY ──
        self.parry_charges = 0   # Quantas cargas de parry acumuladas (max 3)

    def handle_input(self):
        # Verifica quais teclas estão pressionadas nesse frame
        keys = pygame.key.get_pressed()

        # Movimento horizontal
        if keys[pygame.K_a]:
            self.rect.x -= self.speed   # Move pra esquerda
        if keys[pygame.K_d]:
            self.rect.x += self.speed   # Move pra direita

        # Pulo — só pula se estiver no chão
        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = PLAYER_JUMP_FORCE  # Aplica força pra cima
            self.on_ground = False

    def apply_gravity(self):
        # A gravidade aumenta a velocidade vertical a cada frame
        # fazendo o Vael acelerar enquanto cai
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Chão temporário — impede o Vael de cair infinitamente
        # por enquanto o chão é a borda inferior da tela
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

    def update(self):
        # update() é chamado todo frame pelo game loop
        # ele chama todos os sistemas do Vael em ordem
        self.handle_input()
        self.apply_gravity()

    def draw(self, screen):
        # Desenha o Vael na tela na posição do rect
        screen.blit(self.image, self.rect)