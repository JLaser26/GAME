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
    "door": pygame.image.load("assets/tiles/door.png").convert_alpha(),  # NEW
}

# -----------------------------
# Map Manager
# -----------------------------
map_manager = MapManager(tile_images, all_sprites, walls, tiles)

# Load base map
map_manager.load("map_01")

# -----------------------------
# Create player ONCE
# -----------------------------
player = Player(0, 0, walls)
player.rect.topleft = map_manager.spawns["spawn_1"]
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

    # Update player separately
    player.update(dt)
    camera.update(player)

    # -----------------------------
    # Door check
    # -----------------------------
    door_result = map_manager.check_door(player)
    if door_result:
        next_map, spawn_id = door_result

        map_manager.load(next_map)

        # IMPORTANT: update player's wall reference
        player.walls = walls
        player.rect.topleft = map_manager.spawns[spawn_id]

    # Draw
    screen.fill(BLACK)
    # Draw tiles first
    for tile in tiles:
        screen.blit(tile.image, camera.apply(tile))

    # Draw player last (on top)
    screen.blit(player.image, camera.apply(player))


    pygame.display.flip()

pygame.quit()
