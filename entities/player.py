import pygame
from settings import (
    PLAYER_SPEED,
    PLAYER_JUMP_FORCE,
    GRAVITY,
    PLAYER_MAX_ASHES,
    PLAYER_WIDTH,
    PLAYER_HEIGHT,
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    WORLD_WIDTH,
    PARRY_RANGE
)

class Player(pygame.sprite.Sprite):

    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill((180, 180, 180))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = PLAYER_SPEED
        self.velocity_y = 0
        self.on_ground = False

        self.ashes = PLAYER_MAX_ASHES
        self.parry_charges = 0

        self.is_dead = False

        self.parry_key_was_pressed = False
        self.veil_key_was_pressed = False

        self.feedback_color = None
        self.feedback_timer = 0

        # ── COOLDOWN DO PARRY ──
        # Impede o jogador de spammar a tecla E sem parar
        self.parry_cooldown_ms = 600
        self.last_parry_time = 0

    def handle_input(self, enemies=None):
        if enemies is None:
            enemies = []

        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            if self.rect.left > 0:
                old_x = self.rect.x
                self.rect.x -= self.speed
                for enemy in enemies:
                    if self.rect.colliderect(enemy.rect):
                        self.rect.x = old_x
                        break

        if keys[pygame.K_d]:
            if self.rect.right < WORLD_WIDTH:
                old_x = self.rect.x
                self.rect.x += self.speed
                for enemy in enemies:
                    if self.rect.colliderect(enemy.rect):
                        self.rect.x = old_x
                        break

        if keys[pygame.K_w] and self.on_ground:
            self.velocity_y = PLAYER_JUMP_FORCE
            self.on_ground = False

    def apply_gravity(self, ground_y):
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        if self.rect.bottom >= ground_y:
            self.rect.bottom = ground_y
            self.velocity_y = 0
            self.on_ground = True

    def get_enemy_in_range(self, enemies):
        for enemy in enemies:
            distance = abs(enemy.rect.centerx - self.rect.centerx)
            if distance <= PARRY_RANGE:
                return enemy
        return None

    def try_parry(self, enemies):
        # Verifica o cooldown — impede spam da tecla
        now = pygame.time.get_ticks()
        if now - self.last_parry_time < self.parry_cooldown_ms:
            return

        self.last_parry_time = now

        for enemy in enemies:
            if enemy.attack_hitbox and self.rect.colliderect(enemy.attack_hitbox):
                if enemy.is_lethal:
                    continue

                if enemy.is_in_parry_window():
                    enemy.already_parried = True
                    enemy.attack_hitbox = None
                    self.parry_charges = min(self.parry_charges + 1, 3)
                    self.feedback_color = (100, 255, 100)
                    self.feedback_timer = pygame.time.get_ticks()
                    return

    def check_hits(self, enemies):
        # Só causa dano se o jogador realmente estava dentro da hitbox
        # no momento em que a janela de ataque se fechou
        for enemy in enemies:
            if enemy.attack_window_just_ended and not enemy.already_parried:
                if enemy.last_attack_hitbox and self.rect.colliderect(enemy.last_attack_hitbox):
                    self.take_hit()

    def take_hit(self):
        self.ashes -= 1
        self.feedback_color = (255, 80, 80)
        self.feedback_timer = pygame.time.get_ticks()

        if self.ashes <= 0:
            self.ashes = 0
            self.is_dead = True

    def try_veil_strike(self, enemies):
        if self.parry_charges < 3:
            return

        target = self.get_enemy_in_range(enemies)

        if target:
            target.take_damage(1)
            self.ashes = min(self.ashes + 1, PLAYER_MAX_ASHES)

        self.parry_charges = 0

    def handle_combat_input(self, enemies):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_e] and not self.parry_key_was_pressed:
            self.try_parry(enemies)
        self.parry_key_was_pressed = keys[pygame.K_e]

        if keys[pygame.K_q] and not self.veil_key_was_pressed:
            self.try_veil_strike(enemies)
        self.veil_key_was_pressed = keys[pygame.K_q]

    def update(self, ground_y, enemies=None):
        if enemies is None:
            enemies = []

        self.handle_input(enemies)
        self.apply_gravity(ground_y)
        self.handle_combat_input(enemies)
        self.check_hits(enemies)

    def draw(self, screen, camera_x):
        draw_x = self.rect.x - camera_x

        now = pygame.time.get_ticks()
        if self.feedback_color and now - self.feedback_timer < 200:
            temp_image = self.image.copy()
            temp_image.fill(self.feedback_color)
            screen.blit(temp_image, (draw_x, self.rect.y))
        else:
            screen.blit(self.image, (draw_x, self.rect.y))