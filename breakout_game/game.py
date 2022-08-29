import pygame

from .settings import *
from .screen_events import ScreenEvents
from .layout import Layout
from .screen_shaker import ScreenShaker


class Game:
    """Class that manage pygame setup and the main loop."""
    def __init__(self):
        pygame.init()

        pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(GAME_TITLE)

        self.clock = pygame.time.Clock()

        self.layout = Layout()

    def run(self) -> None:
        """Main loop."""

        run = True

        while run:
            # Get all events
            all_events = pygame.event.get()

            # Pass all events to every ScreenEvents objects
            ScreenEvents.update_events(all_events)

            # Check quit window
            for event in all_events:
                if event.type == pygame.QUIT:
                    run = False

            # Update layout
            self.layout.update()

            # Update screen shaker
            ScreenShaker.update()

            # Update screen
            pygame.display.update()

            # Delay loop to match FPS
            self.clock.tick(FPS)

        pygame.quit()
        quit()
