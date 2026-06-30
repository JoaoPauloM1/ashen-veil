import pygame
from settings import DUMMY_ATTACK_COOLDOWN, DUMMY_TELEGRAPH_MS, PARRY_WINDOW_MS

class Dummy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((50, 80))
        self.image.fill((100, 30, 30))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.state = "idle"
        self.state_timer = pygame.time.get_ticks()

        self.is_lethal = False
        self.already_parried = False

        # A hitbox de ataque — só existe durante o estado "attacking"
        self.attack_hitbox = None

        # Sinaliza que a janela de ataque acabou de fechar nesse frame
        # usado para verificar dano apenas uma vez, no momento certo
        self.attack_window_just_ended = False

    def update(self):
        now = pygame.time.get_ticks()
        elapsed = now - self.state_timer

        # Reseta a flag todo frame — ela só fica True por 1 frame
        self.attack_window_just_ended = False

        if self.state == "idle":
            self.image.fill((100, 30, 30))
            self.attack_hitbox = None
            if elapsed >= DUMMY_ATTACK_COOLDOWN:
                self.state = "telegraph"
                self.state_timer = now
                self.already_parried = False

        elif self.state == "telegraph":
            self.image.fill((200, 200, 0))
            if elapsed >= DUMMY_TELEGRAPH_MS:
                self.state = "attacking"
                self.state_timer = now

                # Hitbox larga cobrindo os dois lados do dummy
                hitbox_width = 200
                self.attack_hitbox = pygame.Rect(
                    self.rect.centerx - hitbox_width // 2,
                    self.rect.top,
                    hitbox_width,
                    self.rect.height
                )

        elif self.state == "attacking":
            self.image.fill((255, 255, 255))
            if elapsed >= PARRY_WINDOW_MS:
                # A janela está terminando — sinaliza para verificar dano
                self.attack_window_just_ended = True
                self.state = "recovery"
                self.state_timer = now
                self.attack_hitbox = None

        elif self.state == "recovery":
            self.image.fill((80, 80, 80))
            if elapsed >= 500:
                self.state = "idle"
                self.state_timer = now

    def is_in_parry_window(self):
        return self.state == "attacking" and not self.already_parried

    def take_damage(self, amount):
        print(f"Dummy tomou {amount} de dano!")

    def draw(self, screen, camera_x):
        draw_x = self.rect.x - camera_x
        screen.blit(self.image, (draw_x, self.rect.y))

        # DEBUG — mostra a hitbox de ataque visualmente
        if self.attack_hitbox:
            debug_rect = pygame.Rect(
                self.attack_hitbox.x - camera_x,
                self.attack_hitbox.y,
                self.attack_hitbox.width,
                self.attack_hitbox.height
            )
            pygame.draw.rect(screen, (255, 0, 0), debug_rect, 3)