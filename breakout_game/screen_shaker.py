import random
import math


class ScreenShaker:

    offset_x = 0
    offset_y = 0

    max_frame = 1
    remaining_frame = 0
    magnitude = 0

    @classmethod
    def shake_screen(cls, frame: int, magnitude: int):
        cls.max_frame = frame
        cls.remaining_frame = frame
        cls.magnitude = magnitude

    @classmethod
    def reset(cls):
        cls.max_frame = 1
        cls.remaining_frame = 0
        cls.magnitude = 0
        cls.offset_x = 0
        cls.offset_y = 0
    
    @classmethod
    def update(cls):
        if cls.remaining_frame:
            angle = math.radians(random.randint(0, 359))
            mag = cls.magnitude * (cls.remaining_frame / cls.max_frame)
            cls.offset_x = round(math.cos(angle) * mag)
            cls.offset_y = round(math.sin(angle) * mag)

        cls.remaining_frame = max(cls.remaining_frame - 1, 0)
