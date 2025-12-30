# main.py
import pygame
from settings import *
from player import Player
from camera import Camera
from map_manager import MapManager
from core.asset_manager import AssetManager

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
# Asset manager
# --------------------------------------------------
assets = AssetManager()

# --------------------------------------------------
# Map manager
# --------------------------------------------------
map_manager = MapManager(
    assets=assets,
    all_sprites=all_sprites,
    walls=walls,
    tiles=tiles
)

# load base map
map_manager.load("city_main", theme="city")

# --------------------------------------------------
# Player (created ONCE)
# --------------------------------------------------
player = Player(0, 0, walls)
player.rect.topleft = map_manager.spawns.get("spawn_1", (64, 64))
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

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    player.update(dt)
    camera.update(player)
    map_manager.update(dt)

    # portal logic
    next_map = map_manager.check_portal(player)
    if next_map:
        map_manager.load(next_map, theme="dungeon")
        player.walls = walls
        player.rect.topleft = map_manager.spawns.get("spawn_1", (64, 64))

    # draw
    screen.fill(BLACK)

    for tile in tiles:
        screen.blit(tile.image, camera.apply(tile))

    screen.blit(player.image, camera.apply(player))

    pygame.display.flip()

pygame.quit()
