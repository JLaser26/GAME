# camera.py
import pygame
from settings import WIDTH, HEIGHT

class Camera:
    def __init__(self):
        self.offset = pygame.Vector2()

    def update(self, target):
        self.offset.x = target.rect.centerx - WIDTH // 2
        self.offset.y = target.rect.centery - HEIGHT // 2

    def apply(self, sprite):
        return sprite.rect.move(-self.offset.x, -self.offset.y)
