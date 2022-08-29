import pygame

from .screen_events import ScreenEvents
from .screen_shaker import ScreenShaker
from .settings import *


class Paddle(ScreenEvents, ScreenShaker):
    """Paddle that can be controlled and drawn"""
    def __init__(self, x: int, width: int):
        super().__init__()
        self.width = width

        self.surf = pygame.Surface((self.width, PADDLE_HEIGHT))
        y = self.screen_height - 10
        self.rect = self.surf.get_rect(midbottom=(x, y))

        self.surf.fill(PADDLE_COLOR)

        self.speed = PADDLE_SPEED

    def draw(self) -> None:
        self.screen.blit(self.surf, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))

    def input(self) -> None:
        keys = pygame.key.get_pressed()

        if keys[pygame.K_q]:
            self.rect.centerx -= self.speed
        if keys[pygame.K_d]:
            self.rect.centerx += self.speed

        # Check wall collisions
        self.check_wall_collisions()

    def check_wall_collisions(self) -> None:
        self.rect.left = max(0, self.rect.left)
        self.rect.right = min(self.screen_width, self.rect.right)


    def update(self) -> None:
        self.input()
        self.draw()
