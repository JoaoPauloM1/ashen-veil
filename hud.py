import pygame
import os
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYER_MAX_ASHES

class HUD:
    def __init__(self):
        def load(filename):
            path = os.path.join("assets", "images", "hud", filename)
            return pygame.image.load(path).convert_alpha()

        self.ash_icon        = load("ashes.png")
        self.charge_icon     = load("charge.png")
        self.veil_active     = load("veil-strike-active.png")
        self.veil_inactive   = load("veil-strike-desactive.png")

        self.ash_icon      = pygame.transform.scale(self.ash_icon, (64, 64))
        self.charge_icon   = pygame.transform.scale(self.charge_icon, (52, 52))
        self.veil_active   = pygame.transform.scale(self.veil_active, (80, 80))
        self.veil_inactive = pygame.transform.scale(self.veil_inactive, (80, 80))

        # Versão "vazia" do ícone de Ash — mesma imagem mas bem escurecida
        # simula a Ash perdida sem precisar de um arquivo novo
        self.ash_icon_empty = self.ash_icon.copy()
        self.ash_icon_empty.fill((60, 60, 60, 255), special_flags=pygame.BLEND_RGBA_MULT)

        self.margin       = 40
        self.icon_spacing = 12
        self.padding      = 18

        # ── PAINEL FIXO ──
        # Calculado UMA VEZ usando o máximo de Ashes — nunca muda de tamanho
        self.panel_width = max(
            PLAYER_MAX_ASHES * self.ash_icon.get_width() + (PLAYER_MAX_ASHES - 1) * self.icon_spacing,
            self.veil_active.get_width()
        ) + self.padding * 2

        self.panel_height = (
            self.ash_icon.get_height() +
            self.icon_spacing +
            self.charge_icon.get_height() +
            self.icon_spacing +
            self.veil_active.get_height() +
            self.padding * 2
        )

        self.panel_x = self.margin - self.padding
        self.panel_y = self.margin - self.padding

    def draw_panel(self, screen):
        panel = pygame.Surface((self.panel_width, self.panel_height), pygame.SRCALPHA)

        pygame.draw.rect(panel, (18, 12, 28, 190), (0, 0, self.panel_width, self.panel_height), border_radius=14)
        pygame.draw.rect(panel, (90, 60, 130, 220), (0, 0, self.panel_width, self.panel_height), width=3, border_radius=14)

        inner_margin = 5
        pygame.draw.rect(
            panel, (140, 110, 180, 140),
            (inner_margin, inner_margin, self.panel_width - inner_margin * 2, self.panel_height - inner_margin * 2),
            width=1, border_radius=10
        )

        corner_radius = 3
        corner_color = (170, 140, 210, 200)
        corners = [
            (8, 8),
            (self.panel_width - 8, 8),
            (8, self.panel_height - 8),
            (self.panel_width - 8, self.panel_height - 8),
        ]
        for cx, cy in corners:
            pygame.draw.circle(panel, corner_color, (cx, cy), corner_radius)

        screen.blit(panel, (self.panel_x, self.panel_y))

    def draw(self, screen, ashes, parry_charges):
        # Painel sempre no mesmo lugar, mesmo tamanho
        self.draw_panel(screen)

        # ── ASHES (topo) — sempre desenha os 3 slots, cheio ou vazio ──
        ash_y = self.margin
        for i in range(PLAYER_MAX_ASHES):
            x = self.margin + i * (self.ash_icon.get_width() + self.icon_spacing)
            if i < ashes:
                screen.blit(self.ash_icon, (x, ash_y))
            else:
                screen.blit(self.ash_icon_empty, (x, ash_y))

        # ── PARRY CHARGES (abaixo das ashes) ──
        charges_y = ash_y + self.ash_icon.get_height() + self.icon_spacing
        for i in range(parry_charges):
            x = self.margin + i * (self.charge_icon.get_width() + self.icon_spacing)
            screen.blit(self.charge_icon, (x, charges_y))

        # ── VEIL STRIKE (abaixo das parry charges) ──
        veil_icon = self.veil_active if parry_charges >= 3 else self.veil_inactive
        veil_x = self.margin - 6
        veil_y = charges_y + self.charge_icon.get_height() + self.icon_spacing
        screen.blit(veil_icon, (veil_x, veil_y))