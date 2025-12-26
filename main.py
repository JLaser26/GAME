# main.py
import pygame
from settings import *
from tilemap import MAP, Wall
from player import Player
from camera import Camera

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Starter")
clock = pygame.time.Clock()

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()

# Build map
for row, line in enumerate(MAP):
    for col, char in enumerate(line):
        if char == "1":
            wall = Wall(col * TILESIZE, row * TILESIZE)
            walls.add(wall)
            all_sprites.add(wall)

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
