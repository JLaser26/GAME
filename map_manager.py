# map_manager.py
import os
import json
import pygame

from settings import TILESIZE
from tilemap import Tile
from portal_registry import PORTAL_LINKS


class MapManager:
    def __init__(self, assets, all_sprites, walls, tiles):
        self.assets = assets
        self.all_sprites = all_sprites
        self.walls = walls
        self.tiles = tiles

        self.current_map = None
        self.theme = "city"   # default theme

        self.spawns = {}
        self.portals = []
        self.portal_cooldown = 0

    # --------------------------------------------------
    def load(self, map_name, theme="city"):
        self.current_map = map_name
        self.theme = theme

        # remove old tiles
        for sprite in list(self.tiles):
            self.all_sprites.remove(sprite)

        self.tiles.empty()
        self.walls.empty()
        self.portals.clear()
        self.spawns.clear()

        # ---------- load map ----------
        map_path = os.path.join("maps", f"{map_name}.map")
        with open(map_path, "r") as f:
            map_data = [line.rstrip("\n") for line in f]

        for row, line in enumerate(map_data):
            for col, char in enumerate(line):
                x, y = col * TILESIZE, row * TILESIZE

                if char == "W":
                    tile = Tile(
                        self.assets.get_image(f"{self.theme}.wall_house"),
                        x, y, True
                    )
                    self.walls.add(tile)

                elif char == "D":
                    tile = Tile(
                        self.assets.get_image(f"{self.theme}.door"),
                        x, y, False
                    )

                else:
                    tile = Tile(
                        self.assets.get_image(f"{self.theme}.floor_grass"),
                        x, y, False
                    )

                self.tiles.add(tile)
                self.all_sprites.add(tile)

        # ---------- load metadata ----------
        meta_path = os.path.join("maps", f"{map_name}.meta")
        if os.path.exists(meta_path):
            with open(meta_path, "r") as f:
                meta = json.load(f)

            # spawns
            for name, (row, col) in meta.get("spawns", {}).items():
                self.spawns[name] = (col * TILESIZE, row * TILESIZE)

            # portals
            for key, pid in meta.get("portals", {}).items():
                row, col = eval(key)
                rect = pygame.Rect(
                    col * TILESIZE,
                    row * TILESIZE,
                    TILESIZE,
                    TILESIZE
                )
                self.portals.append({"id": pid, "rect": rect})

    # --------------------------------------------------
    def update(self, dt):
        if self.portal_cooldown > 0:
            self.portal_cooldown -= dt

    # --------------------------------------------------
    def check_portal(self, player):
        if self.portal_cooldown > 0:
            return None

        for portal in self.portals:
            if player.rect.colliderect(portal["rect"]):
                pid = portal["id"]
                if pid in PORTAL_LINKS:
                    self.portal_cooldown = 0.5
                    return PORTAL_LINKS[pid]

        return None
