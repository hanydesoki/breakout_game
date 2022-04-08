import pygame

class Bar:
    """Class managing bar"""

    WIDTH = 100
    HEIGHT = 15

    BAR_COLOR = (200, 200, 200)

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.init()

    def init(self):

        self.width = self.WIDTH
        self.height = self.HEIGHT

        self.surf = pygame.Surface((self.width, self.height))
        self.surf.fill(self.BAR_COLOR)

        x = self.screen.get_width() // 2
        y = int(self.screen.get_height() * 0.95)

        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self):
        self.screen.blit(self.surf, self.rect)

    def move(self):
        # Following mouse position
        x = pygame.mouse.get_pos()[0]
        self.rect.centerx = x

        # Limitation in border
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, self.screen.get_width())

    def update(self):
        self.move()
        self.draw()