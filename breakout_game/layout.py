from .bar import Bar
from .ball import Ball

import pygame

class Layout:
    """Class that manage layout setup and interactions between objects"""

    BACKGROUND_COLOR = (0, 0, 50)

    INIT_BALL_ANGLE = 45

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.background = pygame.Surface(self.screen.get_size())
        self.background.fill(self.BACKGROUND_COLOR)

        self.bar = Bar()

        ball_pos_x = self.bar.rect.centerx
        ball_pos_y = self.bar.rect.top - Ball.RADIUS

        self.ball = Ball(self, self.bar, x=ball_pos_x, y=ball_pos_y)
        self.ball.set_speeds_from_angle(self.INIT_BALL_ANGLE)

        self.launching = True

    def set_ball_to_bar(self):
        ball_pos_x = self.bar.rect.centerx
        ball_pos_y = self.bar.rect.top - Ball.RADIUS

        self.ball.set_ball_pos(ball_pos_x, ball_pos_y)

    def input(self):
        if pygame.mouse.get_pressed()[0]:
            self.launching = False

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def update(self):
        self.draw_background()
        self.bar.update()
        self.ball.update()

        self.input()

        if self.launching:
            self.set_ball_to_bar()
