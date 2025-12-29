# map_manager.py
import os
import json
import pygame

from settings import TILESIZE
from tilemap import Tile
from portal_registry import PORTAL_LINKS


class MapManager:
    def __init__(self, tile_images, all_sprites, walls, tiles):
        self.tile_images = tile_images
        self.all_sprites = all_sprites
        self.walls = walls
        self.tiles = tiles

        self.current_map = None

        # runtime data
        self.spawns = {}        # {"spawn_1": (x, y)}
        self.portals = []       # [{"id": int, "rect": Rect}]
        self.portal_cooldown = 0

    # --------------------------------------------------
    # Load a map (tiles + metadata)
    # --------------------------------------------------
    def load(self, map_name):
        self.current_map = map_name

        # --- remove old tiles (NOT player) ---
        for sprite in list(self.tiles):
            self.all_sprites.remove(sprite)

        self.tiles.empty()
        self.walls.empty()
        self.portals.clear()
        self.spawns.clear()

        # --- load tile layout ---
        map_path = os.path.join("maps", f"{map_name}.map")
        with open(map_path, "r") as f:
            map_data = [line.rstrip("\n") for line in f]

        for row, line in enumerate(map_data):
            for col, char in enumerate(line):
                x = col * TILESIZE
                y = row * TILESIZE

                if char == "W":
                    tile = Tile(self.tile_images["wall"], x, y, solid=True)
                    self.walls.add(tile)

                elif char == "B":
                    tile = Tile(self.tile_images["building"], x, y, solid=True)

                elif char == "T":
                    tile = Tile(self.tile_images["tree"], x, y, solid=True)

                else:
                    tile = Tile(self.tile_images["floor"], x, y, solid=False)

                self.tiles.add(tile)
                self.all_sprites.add(tile)

        # --- load metadata ---
        meta_path = os.path.join("maps", f"{map_name}.meta")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)

            # spawns
            for name, (row, col) in meta.get("spawns", {}).items():
                self.spawns[name] = (col * TILESIZE, row * TILESIZE)

            # portals
            for key, pid in meta.get("portals", {}).items():
                # keys were saved as "(row, col)" strings
                row, col = eval(key)
                rect = pygame.Rect(
                    col * TILESIZE,
                    row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )
                self.portals.append({
                    "id": pid,
                    "rect": rect
                })

    # --------------------------------------------------
    # Update (cooldowns etc.)
    # --------------------------------------------------
    def update(self, dt):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= dt

    # --------------------------------------------------
    # Check portal collision
    # --------------------------------------------------
    def check_portal(self, player):
        if self.portal_cooldown > 0:
            return None

        for portal in self.portals:
            if player.rect.colliderect(portal["rect"]):
                pid = portal["id"]

                if pid in PORTAL_LINKS:
                    self.portal_cooldown = 0.5  # seconds
                    return PORTAL_LINKS[pid]

        return None
