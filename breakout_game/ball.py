import pygame

from .screen_events import ScreenEvents
from .settings import *
from .brick import Brick
from .utils import circle_rectangle_intersection, clamp_value
from .value_cycle import ValueCycle
from .screen_shaker import ScreenShaker

from typing import Union
import random

import math


class Ball(ScreenEvents, ScreenShaker):
    """Ball that move on it's own an collide with bricks, paddle and walls."""
    def __init__(self, x: int, y: int, radius: int, layout):
        super().__init__()
        self.x = x
        self.y = y
        self.radius = radius
        self.layout = layout
        self.paddle = layout.paddle

        self.velocity = BALL_VELOCITY

        self.locked = True
        self.sticky = False
        self.angle_cycle = ValueCycle(-MAX_ANGLE, MAX_ANGLE, 2)
        self.angle_cycle.set_random_value()
        self.launch_angle = MAX_ANGLE
        self.x_vel, self.y_vel = self.get_speed_from_angle(random.randint(-MAX_ANGLE, MAX_ANGLE))

        self.collision_enabled = True

        self.double_damage_frame = 0

        self.contact_x = 0

        self.star_frame = 0

        self.launch_frame = 5

    def move(self) -> None:

        if self.locked:
            self.y = self.paddle.rect.top - self.radius
            self.x = self.paddle.rect.centerx + self.contact_x
            self.launch_angle = next(self.angle_cycle)
            return

        # Move ball horizontally
        self.x += self.x_vel

        # Side paddle collision
        if self.collide_with_paddle() and self.collision_enabled:
            if self.x < self.paddle.rect.centerx:
                if self.x_vel < 0:
                    self.x_vel *= 2
                else:
                    self.x_vel *= -1
            else:
                if self.x_vel < 0:
                    self.x_vel *= -1
                else:
                    self.x_vel *= 2

            self.collision_enabled = False
            return

        # Brick horizontal collision
        collided_brick = self.collided_brick()
        if collided_brick is not None:
            if not self.star_frame:
                if self.x_vel <= 0:
                    self.x = collided_brick.rect.right + self.radius
                else:
                    self.x = collided_brick.rect.left - self.radius
                self.x_vel *= -1
            else:
                if collided_brick.unbreakable:
                    if self.x_vel <= 0:
                        self.x = collided_brick.rect.right + self.radius
                    else:
                        self.x = collided_brick.rect.left - self.radius
                    self.x_vel *= -1

            collided_brick.get_hit()

        # Move ball vertically
        self.y += self.y_vel

        # Top paddle collision
        if self.collide_with_paddle() and self.collision_enabled:
            if self.sticky:
                self.contact_x = clamp_value(self.x - self.paddle.rect.centerx, -self.paddle.width // 2 + self.radius,
                                             self.paddle.width // 2 - self.radius)
                self.lock()
            else:
                self.y = self.paddle.rect.top - self.radius
                distance_ratio = (self.paddle.rect.centerx - self.x) / (self.paddle.width // 2)
                new_angle = 90 + MAX_ANGLE * distance_ratio
                self.x_vel, self.y_vel = self.get_speed_from_angle(new_angle)

        # Brick vertical collision
        collided_brick = self.collided_brick()
        if collided_brick is not None:
            if not self.star_frame:
                if self.y_vel <= 0:
                    self.y = collided_brick.rect.bottom + self.radius
                else:
                    self.y = collided_brick.rect.top - self.radius
                self.y_vel *= -1
            else:
                if collided_brick.unbreakable:
                    if self.y_vel <= 0:
                        self.y = collided_brick.rect.bottom + self.radius
                    else:
                        self.y = collided_brick.rect.top - self.radius
                    self.y_vel *= -1

            collided_brick.get_hit()

        self.boundaries_collisions()

    def boundaries_collisions(self) -> None:
        # Left wall collision
        if self.x - self.radius <= 0:
            self.x_vel *= -1
            self.x = self.radius

        # Right wall collision
        if self.x + self.radius >= self.screen_width:
            self.x_vel *= -1
            self.x = self.screen_width - self.radius

        # Top wall collision
        if self.y <= self.radius:
            self.y_vel *= -1
            self.y = self.radius

    def draw(self) -> None:
        color = BALL_COLOR_STICKY if self.sticky else BALL_COLOR
        center = (self.x + self.offset_x, self.y + self.offset_y)
        pygame.draw.circle(surface=self.screen, color=color, center=center, radius=self.radius)

        if self.double_damage_frame:
            pygame.draw.circle(surface=self.screen, color=BALL_COLOR_DAMAGE, center=center,
                               radius=self.radius, width=2)

        if self.star_frame:
            pygame.draw.circle(surface=self.screen, color=BALL_STAR_COLORS[self.star_frame // 5 % 3],
                               center=center,
                               radius=self.radius + 3, width=3)

        if self.locked:
            radians_angle = math.radians(self.launch_angle)
            line_length = LAUNCH_LINE_LENGTH_STICKY if self.sticky else LAUNCH_LINE_LENGTH
            end_x = (self.x - math.sin(radians_angle) * line_length) + self.offset_x
            end_y = self.y - math.cos(radians_angle) * line_length + self.offset_y
            pygame.draw.line(self.screen, LAUNCH_LINE_COLOR, center, (end_x, end_y))

    def get_speed_from_angle(self, degree_angle: float) -> tuple[float, float]:
        radians_angle = math.radians(degree_angle)
        x_vel = math.cos(radians_angle) * self.velocity
        y_vel = - math.sin(radians_angle) * self.velocity
        return x_vel, y_vel

    def collide_with_paddle(self) -> bool:

        if self.paddle.rect.collidepoint((self.x, self.y)):
            return True

        return circle_rectangle_intersection(circle_x=self.x, circle_y=self.y,
                                             radius=self.radius, rectangle=self.paddle.rect)

    def collided_brick(self) -> Union[Brick, None]:
        for brick in self.layout.bricks:
            if brick.rect.collidepoint((self.x, self.y)):
                return brick

            elif circle_rectangle_intersection(circle_x=self.x, circle_y=self.y,
                                radius=self.radius, rectangle=brick.rect):
                return brick

    def unlock(self) -> None:
        self.locked = False
        self.sticky = False
        self.x_vel, self.y_vel = self.get_speed_from_angle(self.launch_angle + 90)
        self.y = self.paddle.rect.top - 1 - self.radius
        self.contact_x = 0

    @property
    def damage(self) -> int:
        return 2 if self.double_damage_frame else 1

    def manage_bonus_frames(self) -> None:
        if not self.star_frame:
            self.double_damage_frame = max(self.double_damage_frame - 1, 0)

        self.star_frame = max(self.star_frame - 1, 0)

    def lock(self) -> None:
        self.locked = True
        self.collision_enabled = True
        self.launch_frame = 5
        if not self.sticky:
            self.angle_cycle.set_random_value()
        else:
            self.angle_cycle.reset()

    def update(self) -> None:
        self.manage_bonus_frames()
        self.move()
        self.draw()


class SecondBall(Ball):

    def __init__(self, x: int, y: int, radius: int, layout):
        super().__init__(x, y, radius, layout)
        self.unlock()
        self.velocity = SECOND_BALL_VELOCITY
        self.x_vel = self.layout.ball.x_vel * (SECOND_BALL_VELOCITY / BALL_VELOCITY)
        self.y_vel = -self.layout.ball.y_vel * (SECOND_BALL_VELOCITY / BALL_VELOCITY)
        self.move_frame = 2

    def draw(self) -> None:
        center = (self.x + self.offset_x, self.y + self.offset_y)
        pygame.draw.circle(surface=self.screen, color=SECOND_BALL_COLOR, center=center, radius=self.radius)
        pygame.draw.circle(surface=self.screen, color="red", center=center, radius=self.radius, width=3)

    def unlock(self) -> None:
        self.locked = False
        self.sticky = False

    def move(self) -> None:
        self.move_frame = max(self.move_frame - 1, 0)
        if self.move_frame == 0:
            super().move()


