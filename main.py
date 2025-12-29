# main.py
import pygame
from settings import *
from player import Player
from camera import Camera
from map_manager import MapManager

# --------------------------------------------------
# Init
# --------------------------------------------------
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Starter")
clock = pygame.time.Clock()

# --------------------------------------------------
# Sprite groups
# --------------------------------------------------
all_sprites = pygame.sprite.Group()
tiles = pygame.sprite.Group()
walls = pygame.sprite.Group()

# --------------------------------------------------
# Load tile images
# --------------------------------------------------
tile_images = {
    "floor": pygame.image.load("assets/tiles/floor.png").convert_alpha(),
    "wall": pygame.image.load("assets/tiles/wall.png").convert_alpha(),
    "tree": pygame.image.load("assets/tiles/tree.png").convert_alpha(),
    "building": pygame.image.load("assets/tiles/building.png").convert_alpha(),
}

# --------------------------------------------------
# Map manager
# --------------------------------------------------
map_manager = MapManager(
    tile_images=tile_images,
    all_sprites=all_sprites,
    walls=walls,
    tiles=tiles
)

# --------------------------------------------------
# Load base map
# --------------------------------------------------
BASE_MAP = "city_main"   # change if needed
map_manager.load(BASE_MAP)

# --------------------------------------------------
# Create player ONCE
# --------------------------------------------------
player = Player(0, 0, walls)

# Spawn player (fallback safety)
spawn_pos = map_manager.spawns.get("spawn_1", (64, 64))
player.rect.topleft = spawn_pos

all_sprites.add(player)

# --------------------------------------------------
# Camera
# --------------------------------------------------
camera = Camera()

# --------------------------------------------------
# Game loop
# --------------------------------------------------
running = True
while running:
    dt = clock.tick(FPS) / 1000

    # -----------------------------
    # Events
    # -----------------------------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # -----------------------------
    # Update
    # -----------------------------
    player.update(dt)
    camera.update(player)
    map_manager.update(dt)

    # -----------------------------
    # Portal handling
    # -----------------------------
    portal_result = map_manager.check_portal(player)
    if portal_result:
        next_map = portal_result

        map_manager.load(next_map)

        # update collision reference
        player.walls = walls

        # move player to spawn
        spawn_pos = map_manager.spawns.get("spawn_1", (64, 64))
        player.rect.topleft = spawn_pos

    # -----------------------------
    # Draw
    # -----------------------------
    screen.fill(BLACK)

    # draw tiles first
    for tile in tiles:
        screen.blit(tile.image, camera.apply(tile))

    # draw player last
    screen.blit(player.image, camera.apply(player))

    pygame.display.flip()

pygame.quit()