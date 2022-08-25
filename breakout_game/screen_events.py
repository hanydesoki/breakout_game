import pygame


class ScreenEvents:

    all_events = []

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_size = self.screen.get_size()

    @classmethod
    def update_events(cls, all_events) -> None:
        cls.all_events = all_events

    def key_pressed(self, key) -> bool:
        for event in self.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key == key:
                    return True

        return False
