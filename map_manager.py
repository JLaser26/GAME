# map_manager.py
from tilemap import Tile, load_map
from settings import TILESIZE
from door_links import DOOR_LINKS

class MapManager:
    def __init__(self, tile_images, all_sprites, walls, tiles):
        self.tile_images = tile_images
        self.all_sprites = all_sprites
        self.walls = walls
        self.tiles = tiles

        self.doors = []
        self.spawns = {}
        self.current_map = None

    def load(self, map_name):
        # Remove old tiles (NOT player)
        for sprite in list(self.tiles):
            self.all_sprites.remove(sprite)

        self.tiles.empty()
        self.walls.empty()
        self.doors.clear()
        self.spawns.clear()

        map_data = load_map(f"maps/{map_name}.txt")
        self.current_map = map_name

        for row, line in enumerate(map_data):
            for col, char in enumerate(line):
                x, y = col * TILESIZE, row * TILESIZE

                if char == "W":
                    tile = Tile(self.tile_images["wall"], x, y, True)
                    self.walls.add(tile)

                elif char == "D":
                    tile = Tile(self.tile_images["door"], x, y, False)
                    self.doors.append((col, row, tile))

                elif char == "S":
                    tile = Tile(self.tile_images["floor"], x, y)
                    self.spawns["spawn_1"] = (x, y)

                else:
                    tile = Tile(self.tile_images["floor"], x, y)

                self.tiles.add(tile)
                self.all_sprites.add(tile)

    def check_door(self, player):
        for col, row, tile in self.doors:
            if player.rect.colliderect(tile.rect):
                print(f"Touching door at {col, row} in {self.current_map}")
                key = (self.current_map, (col, row))
                print("Checking key:", key)

                if key in DOOR_LINKS:
                    print("Door link FOUND")
                    return DOOR_LINKS[key]
                else:
                    print("Door link NOT found")

        return None

