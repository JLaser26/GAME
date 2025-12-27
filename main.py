# main.py
import pygame
from settings import *
from tilemap import Tile, load_map
from player import Player
from camera import Camera

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
floor_img = pygame.image.load("assets/tiles/floor.png").convert_alpha()
wall_img = pygame.image.load("assets/tiles/wall.png").convert_alpha()
tree_img = pygame.image.load("assets/tiles/tree.png").convert_alpha()
building_img = pygame.image.load("assets/tiles/building.png").convert_alpha()

# -----------------------------
# Load map from file
# -----------------------------
map_data = load_map("maps/map_01.txt")

for row, line in enumerate(map_data):
    for col, char in enumerate(line):
        x = col * TILESIZE
        y = row * TILESIZE

        if char == "W":
            tile = Tile(wall_img, x, y, solid=True)
            walls.add(tile)

        elif char == "T":
            tile = Tile(tree_img, x, y, solid=True)

        elif char == "B":
            tile = Tile(building_img, x, y, solid=True)

        else:  # floor
            tile = Tile(floor_img, x, y, solid=False)

        tiles.add(tile)
        all_sprites.add(tile)

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
