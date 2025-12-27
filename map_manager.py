# map_manager.py
import pygame
from tilemap import Tile, load_map
from settings import TILESIZE

class MapManager:
    def __init__(self, tile_images, all_sprites, walls, tiles):
        self.tile_images = tile_images
        self.all_sprites = all_sprites
        self.walls = walls
        self.tiles = tiles

        self.current_map = None

    def load(self, map_name):
        """Load a map by name (without .txt)"""

        # Clear old tiles
        self.tiles.empty()
        self.walls.empty()

        # Remove old tiles from all_sprites
        for sprite in list(self.all_sprites):
            if sprite in self.tiles or sprite in self.walls:
                self.all_sprites.remove(sprite)

        map_data = load_map(f"maps/{map_name}.txt")
        self.current_map = map_name

        for row, line in enumerate(map_data):
            for col, char in enumerate(line):
                x = col * TILESIZE
                y = row * TILESIZE

                if char == "W":
                    tile = Tile(self.tile_images["wall"], x, y, solid=True)
                    self.walls.add(tile)

                elif char == "T":
                    tile = Tile(self.tile_images["tree"], x, y, solid=True)

                elif char == "B":
                    tile = Tile(self.tile_images["building"], x, y, solid=True)

                else:
                    tile = Tile(self.tile_images["floor"], x, y, solid=False)

                self.tiles.add(tile)
                self.all_sprites.add(tile)
