import pygame
import os
import json

# -----------------------------
# CONFIG
# -----------------------------
TILESIZE = 32
ROWS, COLS = 30, 50
WIDTH, HEIGHT = COLS * TILESIZE, ROWS * TILESIZE

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MAP_DIR = os.path.join(BASE_DIR, "..", "maps")

TILES = {
    ".": (200, 200, 200),  # floor
    "W": (100, 100, 100),  # wall
    "B": (150, 75, 0),     # building
    "T": (0, 150, 0),      # tree
    "P": (0, 0, 255),      # portal
    "S": (255, 255, 0),    # spawn
}

current_tile = "W"
portal_id_counter = 1
portal_data = {}   # {(row,col): portal_id}

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("RPG City Map Editor")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 22)

grid = [["." for _ in range(COLS)] for _ in range(ROWS)]
mouse_down = False

# -----------------------------
# SAVE MAP
# -----------------------------
def save_map():
    os.makedirs(MAP_DIR, exist_ok=True)
    name = input("Map name: ").strip()

    if not name:
        return

    # Save tile map
    with open(os.path.join(MAP_DIR, f"{name}.map"), "w") as f:
        for row in grid:
            f.write("".join(row) + "\n")

    # Save metadata
    meta = {
        "portals": portal_data,
    }

    with open(os.path.join(MAP_DIR, f"{name}.meta"), "w") as f:
        json.dump(meta, f, indent=4)

    print(f"Saved map '{name}'")

# -----------------------------
# MAIN LOOP
# -----------------------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: current_tile = "."
            if event.key == pygame.K_2: current_tile = "W"
            if event.key == pygame.K_3: current_tile = "B"
            if event.key == pygame.K_4: current_tile = "T"
            if event.key == pygame.K_5: current_tile = "P"
            if event.key == pygame.K_6: current_tile = "S"
            if event.key == pygame.K_s: save_map()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    if mouse_down:
        x, y = pygame.mouse.get_pos()
        col, row = x // TILESIZE, y // TILESIZE

        if 0 <= row < ROWS and 0 <= col < COLS:
            grid[row][col] = current_tile

            if current_tile == "P":
                if (row, col) not in portal_data:
                    portal_data[(row, col)] = portal_id_counter
                    portal_id_counter += 1

    # -----------------------------
    # DRAW
    # -----------------------------
    screen.fill((30, 30, 30))

    for r in range(ROWS):
        for c in range(COLS):
            tile = grid[r][c]
            rect = pygame.Rect(c*TILESIZE, r*TILESIZE, TILESIZE, TILESIZE)
            pygame.draw.rect(screen, TILES[tile], rect)
            pygame.draw.rect(screen, (50, 50, 50), rect, 1)

            if tile == "P":
                pid = portal_data.get((r, c), "?")
                text = font.render(str(pid), True, (255,255,255))
                screen.blit(text, rect.topleft)

    info = font.render(
        f"Tile:{current_tile} | 1-. 2-W 3-B 4-T 5-P 6-S | Drag mouse | S-save",
        True, (255,255,255)
    )
    screen.blit(info, (10, HEIGHT-25))

    pygame.display.flip()

pygame.quit()
