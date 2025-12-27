# tilemap.py
import pygame
from settings import TILESIZE

MAP = [
    "WWWWWWWWWWWWWWWW",
    "W..............W",
    "W....WWW.......W",
    "W..............W",
    "W......WW......W",
    "W..............W",
    "WWWWWWWWWWWWWWWW",
]

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, solid=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = solid
