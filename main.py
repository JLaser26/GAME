# main.py
import pygame
from settings import *
from player import Player
from camera import Camera
from map_manager import MapManager

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Starter")
clock = pygame.time.Clock()

# Sprite groups
all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
tiles = pygame.sprite.Group()

# -----------------------------
# Load tile images
# -----------------------------
tile_images = {
    "floor": pygame.image.load("assets/tiles/floor.png").convert_alpha(),
    "wall": pygame.image.load("assets/tiles/wall.png").convert_alpha(),
    "tree": pygame.image.load("assets/tiles/tree.png").convert_alpha(),
    "building": pygame.image.load("assets/tiles/building.png").convert_alpha(),
}

# -----------------------------
# Create Map Manager
# -----------------------------
map_manager = MapManager(
    tile_images=tile_images,
    all_sprites=all_sprites,
    walls=walls,
    tiles=tiles
)

# Load base map
map_manager.load("map_01")

# -----------------------------
# Create player
# -----------------------------
player = Player(64, 64, walls)
all_sprites.add(player)

# -----------------------------
# Camera
# -----------------------------
camera = Camera()

# -----------------------------
# Game loop
# -----------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update
    all_sprites.update(dt)
    camera.update(player)

    # Draw
    screen.fill(BLACK)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    pygame.display.flip()

pygame.quit()
