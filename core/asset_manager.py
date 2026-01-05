# core/asset_manager.py
import pygame
import os


class AssetManager:
    def __init__(self, base_path="assets"):
        self.base_path = base_path
        self._images = {}   # cache

    def get_image(self, key):
        """
        key format: 'city.floor_grass'
        """
        if key in self._images:
            return self._images[key]

        path = self._resolve_path(key)
        image = pygame.image.load(path).convert_alpha()
        self._images[key] = image
        return image

    def _resolve_path(self, key):
        """
        'city.floor_grass' → assets/city/floor_grass.png
        """
        parts = key.split(".")
        folder = parts[0]
        filename = parts[1] + ".png"

        path = os.path.join(self.base_path, folder, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f"Asset not found: {path}")

        return path

    def clear_cache(self):
        """Optional : free memory if needed"""
        self._images.clear()
