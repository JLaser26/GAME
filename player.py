# player.py
import pygame
from settings import PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, walls):
        super().__init__()

        self.image = pygame.image.load(
            "assets/player.png"
        ).convert_alpha()

        self.rect = self.image.get_rect(topleft=(x, y))

        self.walls = walls
        self.vx = 0
        self.vy = 0

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = self.vy = 0

        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
        if keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
        if keys[pygame.K_d]:
            self.vx = PLAYER_SPEED

    def move(self, dt):
        self.rect.x += self.vx * dt
        self.collide("x")
        self.rect.y += self.vy * dt
        self.collide("y")

    def collide(self, direction):
        for wall in self.walls:
            if self.rect.colliderect(wall.rect):
                if direction == "x":
                    if self.vx > 0:
                        self.rect.right = wall.rect.left
                    if self.vx < 0:
                        self.rect.left = wall.rect.right
                if direction == "y":
                    if self.vy > 0:
                        self.rect.bottom = wall.rect.top
                    if self.vy < 0:
                        self.rect.top = wall.rect.bottom

    def update(self, dt):
        self.handle_input()
        self.move(dt)
