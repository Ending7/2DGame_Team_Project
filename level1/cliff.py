import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
from level1 import cycling_mode


class Cliff:
    def __init__(self, cliffX, cliffY, cliffX2, cliffY2):
        self.x = cliffX
        self.y = cliffY
        self.x2 = cliffX2
        self.y2 = cliffY2

    def draw(self):
        draw_rectangle(*self.get_bb())

    def update(self):

        pass

    def get_bb(self):
        return self.x, self.y, self.x2, self.y2

    def handle_collision(self, group, other):
        pass
