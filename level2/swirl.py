import random

from pico2d import load_image, draw_rectangle

import game_framework
from level2 import swimming_mode

class Swirl:
    def __init__(self, swirlX, swirlY, size):
        self.image = load_image('./resource/swirl.png')
        self.x = swirlX
        self.y = swirlY
        self.size = size

    def draw(self):
        if self.size == 1:
            self.image.clip_draw(0, 0, 196, 189, self.x, self.y, 196 /  self.size, 189 / self.size)
            draw_rectangle(*self.get_bb())
        elif self.size == 2:
            self.image.clip_draw(0, 0, 196, 189, self.x, self.y, 196 / self.size, 189 / self.size)
            draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def get_bb(self):
        if self.size == 1:
            return self.x -100, self.y - 95, self.x + 100, self.y + 95
        elif self.size == 2:
            return self.x - 50, self.y - 45, self.x + 50, self.y + 45

    def handle_collision(self, group, other):
        pass
