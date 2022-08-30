import pygame

from .screen_events import ScreenEvents
from .settings import *

import sys


class PauseMenu(ScreenEvents):

    def __init__(self, layout):
        super().__init__()

        self.layout = layout
        self.paused = False

        self.background = pygame.Surface(self.screen_size)
        self.background.fill((50, 50, 50))
        self.background.set_alpha(150)
        self.clock = pygame.time.Clock()
        self.frame = 0

    def draw_background(self):
        self.screen.blit(self.background, (0, 0))

    def input(self):

        if self.key_pressed(pygame.K_ESCAPE) and not self.frame:
            if self.paused:
                self.unpause()
            else:
                self.pause()

            self.frame = 2

    def pause(self):
        self.draw_background()
        self.paused = True

    def unpause(self):
        self.paused = False

    def update_frame(self):
        self.frame = max(self.frame - 1, 0)

    def update(self):
        self.input()
        self.update_frame()
        while self.paused:
            self.input()
            ScreenEvents.update_events(pygame.event.get())

            # Check quit game
            for event in self.all_events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.update_frame()
            self.clock.tick(FPS)
            pygame.display.update()

