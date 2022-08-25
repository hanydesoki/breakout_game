import pygame

from .screen_events import ScreenEvents
from .settings import *
from .utils import color_gradient
from .bonus import BONUS_DICT


class Brick(ScreenEvents):

    def __init__(self, x: int, y: int, width: int, height: int, layout, health: int = 3, bonus: str = None):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layout = layout
        self.health = health
        self.bonus = bonus

        self.max_health = health

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(x, y))
        self.surf.fill(CLEAR_BRICK_COLOR)

        self.star_status_frame = 0
        self.font = pygame.font.SysFont('arialblack', 30)

    def draw(self) -> None:
        self.screen.blit(self.surf, self.rect)
        if self.bonus == 'Star':
            color = BALL_STAR_COLORS[self.star_status_frame // 5 % 3]
            text = self.font.render(f'{int(self.star_status_frame / 60)}', True, color)
            rect = text.get_rect(center=self.rect.center)
            self.screen.blit(text, rect)
            pygame.draw.rect(self.screen, rect=self.rect, color=color, width=3)

    def get_hit(self) -> None:
        self.health = max(0, self.health - self.layout.ball.damage)

        if self.layout.ball.star_frame:
            self.health = 0

        if self.health:
            new_color = color_gradient(DARK_BRICK_COLOR, CLEAR_BRICK_COLOR,
                                       self.health, self.max_health)
            self.surf.fill(new_color)
        else:
            if self.bonus is not None:
                self.layout.bonuses.append(BONUS_DICT[self.bonus](*self.rect.center, self.layout))

    def set_brick_star_bonus(self) -> None:
        self.bonus = 'Star'
        self.star_status_frame = FPS * 31

    def manage_star_status(self) -> None:
        if self.bonus == 'Star':
            self.star_status_frame = max(self.star_status_frame - 1, 0)
            if self.star_status_frame == 0:
                self.bonus = None

    @property
    def destroyed(self):
        return self.health <= 0

    def update(self) -> None:
        self.draw()
        self.manage_star_status()

    def __str__(self):
        return f"Brick {self.x}-{self.y} {self.health > 0}"

    def __repr__(self):
        return str(self)
