import pygame

from .screen_events import ScreenEvents
from .settings import *
from .utils import color_gradient, distance_between_two_points
from .bonus import BONUS_DICT
from .screen_shaker import ScreenShaker


class Brick(ScreenEvents, ScreenShaker):

    def __init__(self, x: int, y: int, width: int, height: int, layout, health: int = 3, bonus: str = None,
                 unbreakable: bool = False):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.layout = layout
        self.health = health
        self.bonus = bonus
        self.unbreakable = unbreakable

        self.max_health = health

        self.surf = pygame.Surface((self.width, self.height))
        self.rect = self.surf.get_rect(topleft=(x, y))
        if self.unbreakable:
            self.surf.fill(UNBREAKABLE_BRICK_COLOR)
        else:
            self.surf.fill(CLEAR_BRICK_COLOR)

        self.star_status_frame = 0
        self.tnt_status_frame = 0
        self.star_font = pygame.font.SysFont('arialblack', 10)
        self.tnt_font = pygame.font.SysFont('arialblack', 10)

    def draw(self) -> None:
        self.screen.blit(self.surf, (self.rect.x + self.offset_x, self.rect.y + self.offset_y))

        if not self.unbreakable:

            if self.bonus == 'Star':
                color = BALL_STAR_COLORS[self.star_status_frame // 5 % 3]
                text = self.star_font.render(f'{int(self.star_status_frame / 60)}', True, color)
                rect = text.get_rect(center=self.rect.center)
                self.screen.blit(text, (rect.x + self.offset_x, rect.y + self.offset_y))
                r = self.rect.copy()
                r.x += self.offset_x
                r.y += self.offset_y
                pygame.draw.rect(self.screen, rect=r, color=color, width=2)

            if self.bonus == 'TNT':
                color = BRICK_TNT_COLORS[self.tnt_status_frame // 10 % 2]
                # text1 = self.tnt_font.render(f'TNT', True, color)
                text1 = self.tnt_font.render(f'{int(self.tnt_status_frame / 60)}', True, color)
                # rect1 = text1.get_rect(midtop=self.rect.midtop)
                rect1 = text1.get_rect(center=self.rect.center)
                self.screen.blit(text1, (rect1.x + self.offset_x, rect1.y + self.offset_y))
                # self.screen.blit(text2, rect2)
                r = self.rect.copy()
                r.x += self.offset_x
                r.y += self.offset_y
                pygame.draw.rect(self.screen, rect=r, color=color, width=3)

    def get_hit(self) -> None:
        if not self.unbreakable:
            self.health = max(0, self.health - self.layout.ball.damage)

            if self.layout.ball.star_frame:
                self.health = 0
                ScreenShaker.shake_screen(10, 10)
            elif self.health == 0 and self.layout.ball.double_damage_frame:
                ScreenShaker.shake_screen(10, 10)
            elif self.health == 0:
                ScreenShaker.shake_screen(5, 5)

            if self.health:
                new_color = color_gradient(DARK_BRICK_COLOR, CLEAR_BRICK_COLOR,
                                           self.health, self.max_health)
                self.surf.fill(new_color)
            else:
                if self.bonus is not None:
                    if self.bonus == 'TNT':
                        self.explode_surrounded_bricks()
                    elif self.bonus == 'Secondball':
                        from .ball import SecondBall
                        self.layout.bonuses.append(SecondBall(self.rect.centerx, self.rect.centery, BALL_RADIUS,
                                                              self.layout))
                    else:
                        self.layout.bonuses.append(BONUS_DICT[self.bonus](*self.rect.center, self.layout))
                    self.bonus = None

    def set_bonus(self, bonus: str) -> None:
        self.bonus = bonus

    def set_brick_star_bonus(self) -> None:
        self.bonus = 'Star'
        self.star_status_frame = FPS * 31

    def explode_surrounded_bricks(self):
        for brick in self.layout.bricks:
            if brick.destroyed or brick.unbreakable:
                continue

            if distance_between_two_points(brick.rect.center, self.rect.center) < EXPLOSION_RADIUS:
                while not brick.destroyed:
                    brick.get_hit()

        ScreenShaker.shake_screen(50, 50)

    def set_brick_tnt_bonus(self) -> None:
        self.bonus = 'TNT'
        self.tnt_status_frame = FPS * 31

    def manage_star_status(self) -> None:
        if self.bonus == 'Star':
            self.star_status_frame = max(self.star_status_frame - 1, 0)
            if self.star_status_frame == 0:
                self.bonus = None

    def manage_tnt_status(self) -> None:
        if self.bonus == 'TNT':
            self.tnt_status_frame = max(self.tnt_status_frame - 1, 0)
            if self.tnt_status_frame == 0:
                self.bonus = None

    @property
    def destroyed(self):
        return self.health <= 0 and not self.unbreakable

    def update(self) -> None:
        self.draw()
        self.manage_star_status()
        self.manage_tnt_status()

    def __str__(self):
        return f"Brick {self.x}-{self.y} {self.health > 0}"

    def __repr__(self):
        return str(self)
