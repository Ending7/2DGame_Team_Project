import random

from pico2d import load_image, draw_rectangle

import game_framework
import game_world
import play_mode


class Rock:
    def __init__(self, rockX, rockY):
        self.image = load_image('./resource/rock.png')
        self.x = rockX
        self.y = rockY
        self.speed = random.randint(1, 5)

    def draw(self):
        self.image.draw(self.x, self.y, 40, 40)
        draw_rectangle(*self.get_bb())

    def update(self):
        if play_mode.time_lock == False:
            self.x -= 1 * 100 * game_framework.frame_time * self.speed
        if self.x < 0:
            game_world.remove_object(self)
        pass

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        if group == 'player:rock':
            pass