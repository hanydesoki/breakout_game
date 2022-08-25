import pygame

from .screen_events import ScreenEvents
from .settings import *
from .utils import color_gradient


class Brick(ScreenEvents):
    def __init__(self, x: int, y: int, width: int, height: int, health: int = 3):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health

        self.max_health = health

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill(CLEAR_BRICK_COLOR)

    def draw(self) -> None:
        self.screen.blit(self.surf, self.rect)

    def get_hit(self) -> None:
        self.health = max(0, self.health - 1)
        if self.health:
            new_color = color_gradient(DARK_BRICK_COLOR, CLEAR_BRICK_COLOR,
                                       self.health, self.max_health)

            self.surf.fill(new_color)

    def update(self) -> None:
        self.draw()
