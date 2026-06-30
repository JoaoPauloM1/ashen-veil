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

        self.margin       = 40   # margem maior — desce e afasta da borda
        self.icon_spacing = 12
        self.padding      = 18

    def draw_panel(self, screen, x, y, width, height):
        panel = pygame.Surface((width, height), pygame.SRCALPHA)

        # Fundo escuro arroxeado, mais profundo que preto puro
        pygame.draw.rect(panel, (18, 12, 28, 190), (0, 0, width, height), border_radius=14)

        # Borda externa roxa sutil, como energia sobrenatural
        pygame.draw.rect(panel, (90, 60, 130, 220), (0, 0, width, height), width=3, border_radius=14)

        # Borda interna mais fina e clara, dá efeito de "moldura dupla"
        inner_margin = 5
        pygame.draw.rect(
            panel, (140, 110, 180, 140),
            (inner_margin, inner_margin, width - inner_margin * 2, height - inner_margin * 2),
            width=1, border_radius=10
        )

        # Cantos com pequenos "ornamentos" — círculos sutis nos 4 cantos
        corner_radius = 3
        corner_color = (170, 140, 210, 200)
        corners = [
            (8, 8),
            (width - 8, 8),
            (8, height - 8),
            (width - 8, height - 8),
        ]
        for cx, cy in corners:
            pygame.draw.circle(panel, corner_color, (cx, cy), corner_radius)

        screen.blit(panel, (x, y))

    def draw(self, screen, ashes, parry_charges):
        panel_width = max(
            ashes * self.ash_icon.get_width() + (ashes - 1) * self.icon_spacing if ashes > 0 else self.ash_icon.get_width(),
            self.veil_active.get_width()
        ) + self.padding * 2

        panel_height = (
            self.ash_icon.get_height() +
            self.icon_spacing +
            self.charge_icon.get_height() +
            self.icon_spacing +
            self.veil_active.get_height() +
            self.padding * 2
        )

        panel_x = self.margin - self.padding
        panel_y = self.margin - self.padding

        self.draw_panel(screen, panel_x, panel_y, panel_width, panel_height)

        # ── ASHES (topo) ──
        ash_y = self.margin
        for i in range(ashes):
            x = self.margin + i * (self.ash_icon.get_width() + self.icon_spacing)
            screen.blit(self.ash_icon, (x, ash_y))

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