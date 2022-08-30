import pygame
import cv2

from .screen_events import ScreenEvents
from .paddle import Paddle
from .ball import Ball
from .brick import Brick
from .settings import *
from .bonus import LockBonus, DamageBonus, LiveBonus, AntiLiveBonus, StarBonus
from .screen_shaker import ScreenShaker
from .utils import color_gradient
from .pause_menu import PauseMenu

import random


class Layout(ScreenEvents, ScreenShaker):

    all_bonuses_names = ['Lock', 'Damage', 'Live', 'Antilive', 'Secondball']

    def __init__(self):
        super().__init__()

        self.paddle = Paddle(x=self.screen_width // 2, width=PADDLE_WIDTH)
        self.bricks = []
        self.brick_grid = []
        # self.load_default_level()

        self.level_number = 1

        self.heart_levels = [1, 3, 5]

        self.load_custom_level()

        self.background_surf = pygame.Surface(self.screen_size)
        self.background_surf.fill(BACKGROUND_COLOR)
        self.ball = Ball(x=self.paddle.rect.centerx, y=self.paddle.rect.top - BALL_RADIUS,
                         radius=BALL_RADIUS, layout=self)

        self.lives = LIVES

        self.win_lose_font = pygame.font.SysFont('arialblack', 30)

        self.bonuses = []

        self.frame = 0

        self.star_spawn_frame = random.randint(FPS * 60 - 30, FPS * 60 + 30)
        self.tnt_spawn_frame = random.randint(FPS * 90 - 30, FPS * 90 + 30)
        # self.star_spawn_frame = 10
        # self.tnt_spawn_frame = 20

        self.pause_menu = PauseMenu(layout=self)

    def load_default_level(self) -> None:

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
                brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self, bonus=bonus, health=BRICK_HEALTH)
                self.bricks.append(brick)
                self.brick_grid[-1].append(brick)

    def load_custom_level(self) -> None:

        self.bricks = []
        self.brick_grid = []

        img = self.get_array_from_image(f'Levels/level_{self.level_number}.png')

        for row in range(ROWS):
            self.brick_grid.append([])
            for col in range(COLS):
                if img[row, col] == 1:
                    x = OFFSET_SIDE + col * (BRICK_WIDTH + BRICK_GAP)
                    y = OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                    brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self, health=BRICK_HEALTH)
                    self.bricks.append(brick)
                    self.brick_grid[-1].append(brick)
                elif img[row, col] == 0:
                    self.brick_grid[-1].append(None)
                else:
                    x = OFFSET_SIDE + col * (BRICK_WIDTH + BRICK_GAP)
                    y = OFFSET_TOP + row * (BRICK_HEIGHT + BRICK_GAP)
                    brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, self, health=BRICK_HEALTH, unbreakable=True)
                    self.bricks.append(brick)
                    self.brick_grid[-1].append(brick)

        for brick, bonus in zip(random.choices([b for b in self.bricks if not b.unbreakable],
                                               k=len(self.all_bonuses_names)), self.all_bonuses_names):
            if bonus == "Live" and self.level_number not in self.heart_levels:
                continue
            brick.set_bonus(bonus)

    @staticmethod
    def get_array_from_image(file: str):
        img = cv2.imread(file)
        img = img.mean(axis=2)

        for i in range(ROWS):
            for j in range(COLS):
                if img[i, j] == 255:
                    img[i, j] = 0
                elif img[i, j] == 0:
                    img[i, j] = 1
                else:
                    img[i, j] = -1

        return img

    def get_border_bricks(self) -> list[Brick]:
        border_bricks = []

        for i in range(ROWS):
            for j in range(COLS):
                brick = self.brick_grid[i][j]
                if brick is None:
                    continue
                if brick.destroyed or brick.unbreakable:
                    continue

                if i == 0 or i == ROWS - 1 or j == 0 or j == COLS - 1:
                    border_bricks.append(brick)
                    continue

                top_brick = self.brick_grid[i - 1][j]
                bottom_brick = self.brick_grid[i + 1][j]
                left_brick = self.brick_grid[i][j - 1]
                right_brick = self.brick_grid[i][j + 1]

                if None in [top_brick, bottom_brick, left_brick, right_brick]:
                    border_bricks.append(brick)
                elif any([top_brick.destroyed, bottom_brick.destroyed, left_brick.destroyed, right_brick.destroyed]):
                    border_bricks.append(brick)

        return border_bricks

    def update_bricks(self) -> None:
        self.bricks = [brick for brick in self.bricks if brick.health > 0]

        for brick in self.bricks:
            brick.update()

    def draw_background(self) -> None:
        self.screen.blit(self.background_surf, (0, 0))

    def draw_lives(self):
        for i in range(self.lives - 1):
            rect = self.paddle.rect.copy()
            rect.x += PADDLE_LIVE_WIDTH * i + self.offset_x
            rect.y += PADDLE_LIVE_WIDTH * i + self.offset_y
            rect.width -= 2 * i * PADDLE_LIVE_WIDTH
            rect.height -= 2 * i * PADDLE_LIVE_WIDTH
            color = color_gradient(PADDLE_MAX_LIVE_COLOR, PADDLE_MIN_LIVE_COLOR, i - 1, MAX_LIVES - 1)

            pygame.draw.rect(self.screen, rect=rect, color=color, width=PADDLE_LIVE_WIDTH)

    def check_lose(self) -> None:
        if self.ball.y - self.ball.radius > self.screen_height + 10:
            self.lose_life()
            self.ball.contact_x = 0

    def check_win(self) -> None:
        if len([brick for brick in self.bricks if not brick.unbreakable]) == 0:
            win_text = self.win_lose_font.render(f'You won level {self.level_number}', True, (255, 255, 255))
            win_rect = win_text.get_rect(center=self.screen_center)

            self.screen.blit(win_text, win_rect)
            pygame.display.update()
            pygame.time.delay(2000)

            self.level_number += 1

            if self.level_number > NUMBER_OF_LEVELS:
                win_text = self.win_lose_font.render('Congratulation!', True, (255, 255, 255))
                win_rect = win_text.get_rect(midtop=win_rect.midbottom)

                self.screen.blit(win_text, win_rect)
                pygame.display.update()
                pygame.time.delay(2000)
                self.level_number = 1

                self.reset_game()

            self.reset_game(reset_live=False)

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

            self.screen.blit(lose_paddle_surf, (self.paddle.rect.x + self.offset_x,
                                                self.paddle.rect.y + self.offset_y))

            self.screen.blit(lose_text, lose_rect)

            pygame.display.update()
            pygame.time.delay(2000)
            self.level_number = 1

            self.reset_game()

    def gain_life(self) -> None:
        self.lives = min(self.lives + 1, MAX_LIVES)

    def reset_game(self, reset_live: bool = True):
        self.load_custom_level()
        if reset_live:
            self.lives = LIVES
        self.paddle.rect.centerx = self.screen_center[0]
        self.ball.lock()
        self.bonuses = []
        self.ball.star_frame = 0
        self.ball.double_damage_frame = 0
        self.frame = 0
        self.star_spawn_frame = random.randint(FPS * 60 - 30, FPS * 60 + 30)
        self.tnt_spawn_frame = random.randint(FPS * 90 - 30, FPS * 90 + 30)
        ScreenShaker.reset()

    def input(self):
        if self.ball.locked and self.key_pressed(pygame.K_SPACE) and self.ball.launch_frame == 0:
            self.ball.unlock()

        # if self.key_pressed(pygame.K_x):
        #     self.explode_tnt_brick()

        # if self.key_pressed(pygame.K_c):
        #     ScreenShaker.shake_screen(10, 10)

        # if self.key_pressed(pygame.K_g):
        #     self.bonuses.append(LiveBonus(300, 50, self))

    def update_bonuses(self):
        new_bonuses = []
        for bonus in self.bonuses:

            if bonus.__class__.__name__ == "SecondBall":
                if bonus.y < self.screen_height + 10:
                    if not self.ball.locked:
                        bonus.update()
                    new_bonuses.append(bonus)
                    bonus.draw()
                continue
            else:
                bonus.update()

            if bonus.rect.colliderect(self.paddle.rect):
                if isinstance(bonus, LockBonus):
                    self.ball.sticky = True
                elif isinstance(bonus, DamageBonus):
                    self.ball.double_damage_frame = 60 * 20
                elif isinstance(bonus, LiveBonus):
                    self.gain_life()
                elif isinstance(bonus, AntiLiveBonus):
                    self.lose_life(reset=False)
                elif isinstance(bonus, StarBonus):
                    self.ball.star_frame = FPS * 10
            else:
                new_bonuses.append(bonus)

        self.bonuses = new_bonuses

    def manage_special_brick(self) -> None:
        bricks = [b for b in self.get_border_bricks() if b.bonus is None]
        if self.frame == self.star_spawn_frame and bricks:
            star_brick = random.choice(bricks)
            star_brick.set_brick_star_bonus()

        bricks = [b for b in self.get_border_bricks() if b.bonus is None]

        if self.frame == self.tnt_spawn_frame and bricks:
            tnt_brick = random.choice(bricks)
            tnt_brick.set_brick_tnt_bonus()

    def update_frame(self):
        if not self.ball.locked:
            self.frame += 1
        else:
            self.ball.launch_frame = max(self.ball.launch_frame - 1, 0)

    def explode_tnt_brick(self):
        for brick in self.bricks:
            if brick.bonus == 'TNT':
                brick.explode_surrounded_bricks()

    def update(self) -> None:
        """Run every frame"""
        self.draw_background()
        self.input()
        self.paddle.update()
        self.update_bricks()
        self.manage_special_brick()
        self.ball.update()
        self.update_bonuses()
        self.check_lose()
        self.check_win()
        self.draw_lives()
        self.update_frame()
        self.pause_menu.update()
