# main.py
import pygame
from settings import *
from player import Player
from camera import Camera
from tilemap import MAP, Tile

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Starter")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()


# Load tile images
wall_img = pygame.image.load("assets/tiles/wall.png").convert_alpha()
floor_img = pygame.image.load("assets/tiles/floor.png").convert_alpha()

tiles = pygame.sprite.Group()
walls = pygame.sprite.Group()

for row, line in enumerate(MAP):
    for col, char in enumerate(line):
        x = col * TILESIZE
        y = row * TILESIZE

        if char == "W":
            tile = Tile(wall_img, x, y, solid=True)
            walls.add(tile)
        else:
            tile = Tile(floor_img, x, y)

        tiles.add(tile)
        all_sprites.add(tile)


player = Player(64, 64, walls)
all_sprites.add(player)

camera = Camera()

running = True
while running:
    dt = clock.tick(FPS) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update(dt)
    camera.update(player)

    screen.fill(BLACK)
    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite))

    pygame.display.flip()

pygame.quit()
