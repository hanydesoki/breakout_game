import pygame

from .screen_events import ScreenEvents
from .settings import *
from .brick import Brick
from .utils import circle_rectangle_intersection
from .value_cycle import ValueCycle

from typing import Union


import math


class Ball(ScreenEvents):
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
        self.angle_cycle = ValueCycle(-MAX_ANGLE, MAX_ANGLE, 2)
        self.launch_angle = MAX_ANGLE
        self.x_vel, self.y_vel = self.get_speed_from_angle(self.launch_angle)

        self.collision_enabled = True

    def move(self) -> None:

        if self.locked:
            self.y = self.paddle.rect.top - self.radius
            self.x = self.paddle.rect.centerx
            self.launch_angle = next(self.angle_cycle)
            return

        # Move ball horizontally
        self.x += self.x_vel

        # Side paddle collision
        if self.collide_with_paddle() and self.collision_enabled:
            self.x_vel *= -1
            self.collision_enabled = False
            return

        # Brick horizontal collision
        collided_brick = self.collided_brick()
        if collided_brick is not None:
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
            self.y = self.paddle.rect.top - self.radius
            distance_ratio = (self.paddle.rect.centerx - self.x) / (self.paddle.width // 2)
            new_angle = 90 + MAX_ANGLE * distance_ratio
            self.x_vel, self.y_vel = self.get_speed_from_angle(new_angle)

        # Brick vertical collision
        collided_brick = self.collided_brick()
        if collided_brick is not None:
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
        pygame.draw.circle(surface=self.screen, color=BALL_COLOR, center=(self.x, self.y), radius=self.radius)
        if self.locked:
            radians_angle = math.radians(self.launch_angle)
            end_x = (self.x - math.sin(radians_angle) * LAUNCH_LINE_LENGHT)
            end_y = self.y - math.cos(radians_angle) * LAUNCH_LINE_LENGHT
            pygame.draw.line(self.screen, LAUNCH_LINE_COLOR, (self.x, self.y), (end_x, end_y))

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
        self.x_vel, self.y_vel = self.get_speed_from_angle(self.launch_angle + 90)
        self.y = self.paddle.rect.top - 1 - self.radius

    def lock(self) -> None:
        self.locked = True
        self.angle_cycle.reset()

    def update(self) -> None:
        self.move()
        self.draw()

