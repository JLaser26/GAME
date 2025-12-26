# tilemap.py
import pygame
from settings import TILESIZE, GRAY

# Simple map (1 = wall, 0 = floor)
MAP = [
    "1111111111111111",
    "1000000000000001",
    "1000011111000001",
    "1000000000000001",
    "1000000110000001",
    "1000000000000001",
    "1111111111111111"
]

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((TILESIZE, TILESIZE))
        self.image.fill(GRAY)
        self.rect = self.image.get_rect(topleft=(x, y))
