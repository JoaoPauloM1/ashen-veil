import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MAX_ASHES

class CheckpointSystem:
    def __init__(self):
        # Fonte para a mensagem "Checkpoint..."
        self.font = pygame.font.SysFont("Georgia", 28, italic=True)

        # Slots onde existem checkpoints
        self.checkpoint_slots = [4, 9]

        # Guarda quais checkpoints já foram ativados (pra não repetir a mensagem)
        self.activated = set()

        # Posição salva do último checkpoint — usada pro respawn
        self.saved_slot = 0
        self.saved_ashes = PLAYER_MAX_ASHES

        # Controla a mensagem na tela
        self.message_active = False
        self.message_timer = 0
        self.message_duration = 2000  # 2 segundos na tela

    def check(self, current_slot):
        # Verifica se o jogador entrou em um slot de checkpoint não ativado ainda
        if current_slot in self.checkpoint_slots and current_slot not in self.activated:
            self.activated.add(current_slot)
            self.saved_slot = current_slot
            self.message_active = True
            self.message_timer = pygame.time.get_ticks()

    def update(self):
        if self.message_active:
            now = pygame.time.get_ticks()
            if now - self.message_timer >= self.message_duration:
                self.message_active = False

    def save(self, slot, ashes):
        # Chamado manualmente quando quisermos forçar um save
        self.saved_slot = slot
        self.saved_ashes = PLAYER_MAX_ASHES  # sempre volta com Ashes cheias

    def draw(self, screen, player_rect, camera_x):
        if self.message_active:
            text_surface = self.font.render("Checkpoint...", True, (200, 200, 255))

            # Posiciona acima do Vael, seguindo a posição dele na tela
            draw_x = player_rect.centerx - camera_x - text_surface.get_width() // 2
            draw_y = player_rect.top - 50

            # Fundo escuro semi-transparente atrás do texto
            padding = 10
            bg_rect = pygame.Rect(
                draw_x - padding,
                draw_y - padding,
                text_surface.get_width() + padding * 2,
                text_surface.get_height() + padding * 2
            )
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
            bg_surface.fill((0, 0, 0, 140))
            screen.blit(bg_surface, (bg_rect.x, bg_rect.y))

            screen.blit(text_surface, (draw_x, draw_y))