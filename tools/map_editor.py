import pygame
import sys

TILESIZE = 32
ROWS, COLS = 15, 20
WIDTH, HEIGHT = COLS * TILESIZE, ROWS * TILESIZE

# Tile symbols
TILES = {
    ".": (200, 200, 200),  # floor
    "W": (100, 100, 100),  # wall
    "T": (0, 150, 0),      # tree
    "B": (150, 75, 0),     # building
}

tile_keys = list(TILES.keys())
current_tile = "W"

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG Map Editor")
clock = pygame.time.Clock()

# Create empty map
grid = [["." for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont(None, 24)

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.join(BASE_DIR, "..", "maps")

def save_map():
    os.makedirs(MAP_DIR, exist_ok=True)  # auto-create maps folder

    name = input("Enter map file name (without .txt): ").strip()
    if not name:
        print("Invalid name!")
        return

    path = os.path.join(MAP_DIR, f"{name}.txt")

    with open(path, "w") as f:
        for row in grid:
            f.write("".join(row) + "\n")

    print(f"Map saved at: {path}")


running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                current_tile = tile_keys[0]
            if event.key == pygame.K_2:
                current_tile = tile_keys[1]
            if event.key == pygame.K_3:
                current_tile = tile_keys[2]
            if event.key == pygame.K_4:
                current_tile = tile_keys[3]

            if event.key == pygame.K_s:
                save_map()

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            col = x // TILESIZE
            row = y // TILESIZE
            if 0 <= row < ROWS and 0 <= col < COLS:
                grid[row][col] = current_tile

    screen.fill((30, 30, 30))

    for row in range(ROWS):
        for col in range(COLS):
            tile = grid[row][col]
            color = TILES[tile]
            rect = pygame.Rect(col * TILESIZE, row * TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

    text = font.render(f"Tile: {current_tile} | 1-4 select | S save", True, (255, 255, 255))
    screen.blit(text, (10, HEIGHT - 25))

    pygame.display.flip()

pygame.quit()
sys.exit()
