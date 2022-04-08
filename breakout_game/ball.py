from .bar import Bar
from .utils import get_sign

import pygame

import math

class Ball:
    """Class that manage ball"""
    RADIUS = 10

    BALL_COLOR = (150, 150, 150)

    SPEED = 4

    MAX_ANGLE = 60

    def __init__(self, layout, bar: Bar, x: int, y: int):
        self.screen = pygame.display.get_surface()

        self.layout = layout

        self.bar = bar

        self.rect = pygame.Rect((x, y, self.RADIUS * 2, self.RADIUS * 2))

        self.set_ball_pos(x, y)

    def set_speeds_from_angle(self, angle: float):
        self.vy = max(1, self.SPEED * math.cos(math.radians(angle)))
        self.vx = max(1, self.SPEED * math.sin(math.radians(angle)))

        self.vy = -abs(self.vy)

    def set_ball_pos(self, x: int, y: int):
        self.rect.centerx = x
        self.rect.centery = y

    def move(self):
        self.rect.centerx += self.vx
        self.rect.centery += self.vy

    def draw(self):
        pygame.draw.circle(self.screen, self.BALL_COLOR, center=self.rect.center, radius=self.RADIUS)

    def wall_collisions(self):

        if self.rect.left <= 0: # Collision with left wall
            self.rect.centerx = self.RADIUS + 1
            self.vx *= -1

        if self.rect.right >= self.screen.get_width(): # Collision with left wall
            self.rect.centerx = self.screen.get_width() - self.RADIUS - 1
            self.vx *= -1

        if self.rect.top <= 0: # Collision with left wall
            self.rect.centery = self.RADIUS + 1
            self.vy *= -1

    def bar_collisions(self):
        if self.rect.colliderect(self.bar.rect) and not self.layout.launching:
            self.rect.bottom = self.bar.rect.top

            angle, direction = self.get_angle_from_bar_pos()

            self.set_speeds_from_angle(angle)

            self.vx = abs(self.vx) * direction

            #print(math.sqrt(self.vx**2 + self.vy**2))


    def get_angle_from_bar_pos(self):
        bar_centerx = self.bar.rect.centerx
        ball_centerx = self.rect.centerx

        dist = ball_centerx - bar_centerx
        max_dist = self.bar.rect.left - bar_centerx

        angle = abs(self.MAX_ANGLE * dist / max_dist)
        direction = get_sign(dist)

        print('angle', angle)
        print('dist', dist)
        print('dir', direction)


        return angle, direction

    def check_collisions(self):
        self.wall_collisions()
        self.bar_collisions()

    def update(self):
        self.move()
        self.check_collisions()
        self.draw()



