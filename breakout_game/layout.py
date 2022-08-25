import pygame

from .screen_events import ScreenEvents
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .settings import *
from .bonus import LockBonus, DamageBonus, LiveBonus, AntiLiveBonus

import random


class Layout(ScreenEvents):

    all_bonuses_names = ['Lock', 'Damage', 'Live', 'Antilive']

    def __init__(self):
        super().__init__()

        self.paddle = Paddle(x=self.screen_width // 2, width=PADDLE_WIDTH)
        self.bricks = []
        self.reset_bricks()

        self.background_surf = pygame.Surface(self.screen_size)
        self.background_surf.fill(BACKGROUND_COLOR)
        self.ball = Ball(x=self.paddle.rect.centerx, y=self.paddle.rect.top - BALL_RADIUS,
                         radius=BALL_RADIUS, layout=self)

        self.lives = 2

        self.live_font = pygame.font.SysFont('arial', 20)
        self.win_lose_font = pygame.font.SysFont('arialblack', 30)

        self.bonuses = []

    def reset_bricks(self) -> None:

        self.bricks = []

        bonuses = {}

        for bonus_name in self.all_bonuses_names:
            while True:
                new_pair = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
                if new_pair not in bonuses.values():
                    bonuses[new_pair] = bonus_name
                    break

        for row in range(ROWS):
            for col in range(COLS):
                x = OFFSET_SIDE + col * (BRICK_WIDTH + BRICK_GAP)
                y = OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                bonus = bonuses.get((row, col))
                self.bricks.append(Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self, bonus=bonus))

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
            self.ball.contact_x = 0

    def check_win(self) -> None:
        if len(self.bricks) == 0:
            lose_text = self.win_lose_font.render('You won!', True, (255, 255, 255))
            lose_rect = lose_text.get_rect(center=self.screen_center)

            self.screen.blit(lose_text, lose_rect)
            pygame.display.update()
            pygame.time.delay(2000)

            self.reset_game()

    def lose_life(self, reset: bool = True) -> None:
        self.lives -= 1

        if self.lives and reset:
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

    def update_bonuses(self):
        new_bonuses = []
        for bonus in self.bonuses:
            bonus.update()

            if bonus.rect.colliderect(self.paddle.rect):
                if isinstance(bonus, LockBonus):
                    self.ball.sticky = True
                elif isinstance(bonus, DamageBonus):
                    self.ball.double_damage_frame = 60 * 20
                elif isinstance(bonus, LiveBonus):
                    self.lives += 1
                elif isinstance(bonus, AntiLiveBonus):
                    self.lose_life(reset=False)
            else:
                new_bonuses.append(bonus)

        self.bonuses = new_bonuses

    def update(self) -> None:
        """Run every frame"""
        self.draw_background()
        self.input()
        self.paddle.update()
        self.update_bricks()
        self.ball.update()
        self.update_bonuses()
        self.check_lose()
        self.check_win()
        self.draw_lives()
