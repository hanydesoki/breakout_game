import pygame

from .screen_events import ScreenEvents
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .settings import *
from .bonus import LockBonus, DamageBonus, LiveBonus, AntiLiveBonus, StarBonus

import random


class Layout(ScreenEvents):

    all_bonuses_names = ['Lock', 'Damage', 'Live', 'Antilive']

    def __init__(self):
        super().__init__()

        self.paddle = Paddle(x=self.screen_width // 2, width=PADDLE_WIDTH)
        self.bricks = []
        self.brick_grid = []
        self.reset_bricks()

        self.background_surf = pygame.Surface(self.screen_size)
        self.background_surf.fill(BACKGROUND_COLOR)
        self.ball = Ball(x=self.paddle.rect.centerx, y=self.paddle.rect.top - BALL_RADIUS,
                         radius=BALL_RADIUS, layout=self)

        self.lives = LIVES

        self.live_font = pygame.font.SysFont('arial', 20)
        self.win_lose_font = pygame.font.SysFont('arialblack', 30)

        self.bonuses = []

        self.frame = 0

        self.star_spawn_frame = random.randint(FPS * 60 - 30, FPS * 60 + 30)

    def reset_bricks(self) -> None:

        self.bricks = []
        self.brick_grid = []

        bonuses = {}

        for bonus_name in self.all_bonuses_names:
            while True:
                new_pair = (random.randint(0, ROWS - 1), random.randint(0, COLS - 1))
                if new_pair not in bonuses.values():
                    bonuses[new_pair] = bonus_name
                    break

        for row in range(ROWS):
            self.brick_grid.append([])
            for col in range(COLS):
                x = OFFSET_SIDE + col * (BRICK_WIDTH + BRICK_GAP)
                y = OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                bonus = bonuses.get((row, col))
                brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self, bonus=bonus)
                self.bricks.append(brick)
                self.brick_grid[-1].append(brick)

    def get_border_bricks(self) -> list[Brick]:
        border_bricks = []

        for i in range(ROWS):
            for j in range(COLS):
                brick = self.brick_grid[i][j]
                if brick.destroyed:
                    continue

                if i == 0 or i == ROWS - 1 or j == 0 or j == COLS - 1:
                    border_bricks.append(brick)
                    continue

                elif any([self.brick_grid[i - 1][j].destroyed,
                        self.brick_grid[i + 1][j].destroyed,
                        self.brick_grid[i][j - 1].destroyed,
                        self.brick_grid[i][j + 1].destroyed]):
                    border_bricks.append(brick)

        return border_bricks

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
        self.lives = LIVES
        self.paddle.rect.centerx = self.screen_center[0]
        self.ball.lock()
        self.bonuses = []
        self.ball.star_frame = 0
        self.ball.double_damage_frame = 0
        self.frame = 0
        self.star_spawn_frame = random.randint(FPS * 60 - 30, FPS * 60 + 30)

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
                elif isinstance(bonus, StarBonus):
                    self.ball.star_frame = FPS * 10
            else:
                new_bonuses.append(bonus)

        self.bonuses = new_bonuses

    def manage_star_brick(self) -> None:
        if self.frame == self.star_spawn_frame:
            star_brick = random.choice([b for b in self.get_border_bricks() if b.bonus is None])
            star_brick.set_brick_star_bonus()

    def update_frame(self):
        if not self.ball.locked:
            self.frame += 1

    def update(self) -> None:
        """Run every frame"""
        self.draw_background()
        self.input()
        self.paddle.update()
        self.update_bricks()
        self.manage_star_brick()
        self.ball.update()
        self.update_bonuses()
        self.check_lose()
        self.check_win()
        self.draw_lives()
        self.update_frame()
