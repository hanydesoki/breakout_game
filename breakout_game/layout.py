import pygame

from .screen_events import ScreenEvents
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .settings import *


class Layout(ScreenEvents):

    def __init__(self):
        super().__init__()

        self.paddle = Paddle(x=self.screen_width // 2, width=PADDLE_WIDTH)
        self.bricks = []
        self.reset_bricks()

        self.background_surf = pygame.Surface(self.screen_size)
        self.background_surf.fill(BACKGROUND_COLOR)
        self.ball = Ball(x=self.paddle.rect.centerx, y=self.paddle.rect.top - BALL_RADIUS,
                         radius=BALL_RADIUS, layout=self)

    def reset_bricks(self) -> None:

        self.bricks = []

        for row in range(ROWS):
            for col in range(COLS):
                x = OFFSET_SIDE + col * (BRICK_WIDTH + BRICK_GAP)
                y = OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                self.bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT))

    def update_bricks(self) -> None:
        self.bricks = [brick for brick in self.bricks if brick.health > 0]

        for brick in self.bricks:
            brick.update()

    def draw_background(self) -> None:
        self.screen.blit(self.background_surf, (0, 0))

    def input(self):
        if self.ball.locked and self.key_pressed(pygame.K_SPACE):
            self.ball.unlock()

    def update(self) -> None:
        """Run every frame"""
        self.draw_background()
        self.input()
        self.paddle.update()
        self.ball.update()
        self.update_bricks()
