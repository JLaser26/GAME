# player.py
import pygame
from settings import PLAYER_SPEED

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, walls):
        super().__init__()

        # Load frames
        self.frames = {}
        for direction in ["down", "up", "left", "right"]:
            self.frames[direction] = [
                pygame.image.load(f"assets/{direction}_0.png").convert_alpha(),
                pygame.image.load(f"assets/{direction}_1.png").convert_alpha()
            ]

        self.direction = "down"
        self.frame_index = 0
        self.image = self.frames[self.direction][self.frame_index]
        self.rect = self.image.get_rect(topleft=(x, y))

        self.walls = walls
        self.vx = 0
        self.vy = 0

        # Animation timing
        self.anim_timer = 0
        self.anim_speed = 0.15  # seconds per frame

    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = self.vy = 0
        moving = False

        if keys[pygame.K_w]:
            self.vy = -PLAYER_SPEED
            self.direction = "up"
            moving = True
        elif keys[pygame.K_s]:
            self.vy = PLAYER_SPEED
            self.direction = "down"
            moving = True

        if keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.direction = "left"
            moving = True
        elif keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.direction = "right"
            moving = True

        self.animate(moving)

    def animate(self, moving):
        if moving:
            self.anim_timer += 1 / 60  # approximate frame time
            if self.anim_timer >= self.anim_speed:
                self.anim_timer = 0
                self.frame_index = (self.frame_index + 1) % 2
        else:
            self.frame_index = 0

        self.image = self.frames[self.direction][self.frame_index]

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
