import pygame
from settings import TILESIZE

def load_map(filename):
    with open(filename, "r") as f:
        return [line.strip() for line in f.readlines()]

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, solid=False):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.solid = solid
