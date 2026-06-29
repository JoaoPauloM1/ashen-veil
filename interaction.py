import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SCENE_WIDTH

class InteractionZone:
    def __init__(self, scene_slot, x_start, x_end, label):
        # scene_slot — em qual slot do mundo essa zona existe
        # x_start e x_end — posição local dentro do cenário (0 a SCREEN_WIDTH)
        # label — texto que aparece na tela
        self.scene_slot = scene_slot
        self.x_start = x_start
        self.x_end = x_end
        self.label = label
        self.active = False      # se o jogador está dentro da zona
        self.enabled = True      # se a zona está habilitada (pode ser desabilitada)

    def check(self, player_rect, camera_x):
        if not self.enabled:
            self.active = False
            return

        # Posição do jogador no mundo
        player_world_x = player_rect.centerx

        # Início e fim da zona no mundo
        zone_world_start = self.scene_slot * SCENE_WIDTH + self.x_start
        zone_world_end   = self.scene_slot * SCENE_WIDTH + self.x_end

        # Verifica se o jogador está dentro da zona
        self.active = zone_world_start <= player_world_x <= zone_world_end


class InteractionSystem:
    def __init__(self):
        # Fonte para o texto de interação
        self.font = pygame.font.SysFont("Georgia", 22, italic=True)

        # Animação de pulso do texto
        self.pulse_timer = 0
        self.pulse_alpha = 255

        # Define todas as zonas de interação do mundo
        # Os slots seguem a ordem do scene_order do cemetery.py:
        # 0=cemiterio1, 1,2,3=cemiterio2x3, 4=cemiterio3, 5=cemiterio4,
        # 6,7,8=cemiterio5x3, 9=cemiterio6, 10=cemiterio7
        self.zones = {
            "church_door": InteractionZone(
                scene_slot=4,      # cemiterio3 — entrada da igreja
                x_start=950,
                x_end=1280,
                label="Aperte F para interagir."
            ),
            "well": InteractionZone(
                scene_slot=9,      # cemiterio6 — poço
                x_start=450,
                x_end=830,
                label="Aperte F para interagir."
            ),
            "final_gate": InteractionZone(
                scene_slot=10,     # cemiterio7 — portão final
                x_start=900,
                x_end=1280,
                label="Aperte F para interagir.",
            ),
        }

        # Portão final começa desabilitado — só ativa após derrotar a DEATH
        self.zones["final_gate"].enabled = False

    def update(self, player_rect, camera_x):
        # Atualiza todas as zonas
        for zone in self.zones.values():
            zone.check(player_rect, camera_x)

        # Animação de pulso no texto
        self.pulse_timer += 3
        self.pulse_alpha = int(128 + 127 * abs(pygame.math.Vector2(1, 0).rotate(self.pulse_timer).x))

    def get_active_zone(self):
        # Retorna a zona ativa no momento, se houver
        for name, zone in self.zones.items():
            if zone.active:
                return name, zone
        return None, None

    def draw(self, screen):
        name, zone = self.get_active_zone()
        if zone:
            # Renderiza o texto
            text_surface = self.font.render(zone.label, True, (220, 220, 255))
            text_surface.set_alpha(self.pulse_alpha)

            # Centraliza na tela horizontalmente, posiciona no terço superior
            text_x = SCREEN_WIDTH // 2 - text_surface.get_width() // 2
            text_y = SCREEN_HEIGHT // 3

            # Fundo escuro atrás do texto para legibilidade
            padding = 12
            bg_rect = pygame.Rect(
                text_x - padding,
                text_y - padding,
                text_surface.get_width() + padding * 2,
                text_surface.get_height() + padding * 2
            )
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(140)
            bg_surface.fill((0, 0, 0))
            screen.blit(bg_surface, (bg_rect.x, bg_rect.y))
            screen.blit(text_surface, (text_x, text_y))