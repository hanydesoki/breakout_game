from .layout import Layout

import pygame

import sys

class Game:
    """Class that manage basic pygame setup"""

    SCREEN_WIDTH = 750
    SCREEN_HEIGHT = 500

    FPS = 60

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption('Breakout')
        self.clock = pygame.time.Clock()

        self.layout = Layout()


    def run(self):

        while True:

            all_events = pygame.event.get() # Get all events

            for event in all_events: # Loop in all events
                if event.type == pygame.QUIT: # Check if we hit exit button
                    pygame.quit()
                    sys.exit()


            self.layout.update()

            self.clock.tick(self.FPS)
            pygame.display.update()