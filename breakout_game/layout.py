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

        self.lives = 3

        self.live_font = pygame.font.SysFont('arial', 20)
        self.win_lose_font = pygame.font.SysFont('arialblack', 30)

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

    def draw_lives(self):
        live_text = self.live_font.render('o' * self.lives, True, (0, 0, 0))
        live_rect = live_text.get_rect(center=self.paddle.rect.center)

        self.screen.blit(live_text, live_rect)

    def check_lose(self) -> None:
        if self.ball.y - self.ball.radius > self.screen_height + 10:
            self.lose_life()

    def check_win(self) -> None:
        if len(self.bricks) == 0:
            lose_text = self.win_lose_font.render('You won!', True, (255, 255, 255))
            lose_rect = lose_text.get_rect(center=self.screen_center)

            self.screen.blit(lose_text, lose_rect)
            pygame.display.update()
            pygame.time.delay(2000)

            self.reset_game()

    def lose_life(self) -> None:
        self.lives -= 1

        if self.lives:
            self.ball.lock()

        if self.lives <= 0:
            self.lives = 0
            lose_text = self.win_lose_font.render('You lost...', True, (255, 255, 255))
            lose_rect = lose_text.get_rect(center=self.screen_center)

            lose_paddle_surf = pygame.Surface(self.paddle.surf.get_size())
            lose_paddle_surf.fill(PADDLE_LOSE_COLOR)

            self.screen.blit(lose_paddle_surf, self.paddle.rect)

            self.screen.blit(lose_text, lose_rect)

            pygame.display.update()
            pygame.time.delay(2000)

            self.reset_game()

    def reset_game(self):
        self.reset_bricks()
        self.lives = 3
        self.paddle.rect.centerx = self.screen_center[0]
        self.ball.lock()

    def input(self):
        if self.ball.locked and self.key_pressed(pygame.K_SPACE):
            self.ball.unlock()

    def update(self) -> None:
        """Run every frame"""
        self.draw_background()
        self.input()
        self.ball.update()
        self.paddle.update()
        self.update_bricks()
        self.check_lose()
        self.check_win()
        self.draw_lives()
