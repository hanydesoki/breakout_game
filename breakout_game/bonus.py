import pygame

from .screen_events import ScreenEvents
from .screen_shaker import ScreenShaker


class Bonus(ScreenEvents, ScreenShaker):

    speed = 2

    def __init__(self, x: int, y: int, layout):
        super().__init__()
        self.image = None
        self.rect = None
        self.x = x
        self.y = y
        self.layout = layout

    def move(self):
        self.rect.centery += self.speed

    def draw(self):
        self.screen.blit(self.image, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))

    def update(self):
        self.move()
        self.draw()


class LockBonus(Bonus):

    def __init__(self, x: int, y: int, layout):
        super(LockBonus, self).__init__(x, y, layout)
        self.image = pygame.image.load('Assets/lock.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))


class DamageBonus(Bonus):

    def __init__(self, x: int, y: int, layout):
        super(DamageBonus, self).__init__(x, y, layout)
        self.image = pygame.image.load('Assets/damage.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))


class LiveBonus(Bonus):

    def __init__(self, x: int, y: int, layout):
        super(LiveBonus, self).__init__(x, y, layout)
        self.image = pygame.image.load('Assets/live.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))


class AntiLiveBonus(Bonus):

    def __init__(self, x: int, y: int, layout):
        super(AntiLiveBonus, self).__init__(x, y, layout)
        self.image = pygame.image.load('Assets/anti_live.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))


class StarBonus(Bonus):

    def __init__(self, x: int, y: int, layout):
        super(StarBonus, self).__init__(x, y, layout)
        self.image = pygame.image.load('Assets/star.png').convert_alpha()
        self.image.set_colorkey((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))

BONUS_DICT = {
    'Lock': LockBonus,
    'Damage': DamageBonus,
    'Live': LiveBonus,
    'Antilive': AntiLiveBonus,
    'Star': StarBonus,
}

