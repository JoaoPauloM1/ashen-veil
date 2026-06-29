import pygame
import os
from settings import SCENE_WIDTH, SCENE_HEIGHT, WORLD_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT

class Cemetery:
    def __init__(self):
        self.images = {}
        unique_files = [
            "cemiterio1.png",
            "cemiterio2.png",
            "cemiterio3.png",
            "cemiterio4.png",
            "cemiterio5.png",
            "cemiterio6.png",
            "cemiterio7.png",
        ]
        for filename in unique_files:
            path = os.path.join("assets", "images", "cemetery", filename)
            image = pygame.image.load(path).convert()
            image = pygame.transform.scale(image, (SCREEN_WIDTH, SCREEN_HEIGHT))
            key = filename.replace(".png", "")
            self.images[key] = image

        self.scene_order = [
            "cemiterio1",
            "cemiterio2",
            "cemiterio2",
            "cemiterio2",
            "cemiterio3",
            "cemiterio4",
            "cemiterio5",
            "cemiterio5",
            "cemiterio5",
            "cemiterio6",
            "cemiterio7",
        ]

        self.camera_x = 0

    def update_camera(self, player_rect, slot_left, slot_right):
        # Tenta centralizar o jogador na tela
        target_x = player_rect.centerx - SCREEN_WIDTH // 2

        # Limites da câmera baseados no slot atual
        # mínimo: início do slot (não mostra o slot anterior)
        # máximo: fim do slot menos a tela (não mostra o próximo slot)
        cam_min = slot_left
        cam_max = slot_right - SCREEN_WIDTH

        # Se o slot for menor que a tela, trava no início do slot
        if cam_max < cam_min:
            cam_max = cam_min

        self.camera_x = max(cam_min, min(target_x, cam_max))

    def draw(self, screen):
        for i, scene_key in enumerate(self.scene_order):
            scene_world_x = i * SCENE_WIDTH
            scene_screen_x = scene_world_x - self.camera_x

            if -SCENE_WIDTH < scene_screen_x < SCREEN_WIDTH:
                self.images[scene_key]
                screen.blit(self.images[scene_key], (scene_screen_x, 0))