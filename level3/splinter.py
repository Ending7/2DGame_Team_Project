import random

from pico2d import load_image, draw_rectangle

import game_framework
from level3 import running_mode

TIME_PER_ACTION = 1.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Splinter:
    def __init__(self, splinterX, splinterY, splinter_size, splinter_frame):
        self.image = load_image('./resource/splinter.png')
        self.action = 0
        self.frame = splinter_frame
        self.x = splinterX
        self.y = splinterY
        self.size = splinter_size
        self.speed = random.randint(1, 10)
    def draw(self):
        if self.action == 0:
            self.image.clip_draw(int(self.frame) * 56, self.action * 90, 56, 90, self.x, self.y, 95/self.size, 95/self.size)
            draw_rectangle(*self.get_bb())
        elif self.action == 1:
            self.image.clip_draw(int(self.frame) * 56 , self.action * 90, 56, 90, self.x, self.y, 95/self.size, 95/self.size)
            draw_rectangle(*self.get_bb())


    def update(self):
        if running_mode.time_lock == False:
            self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION

    def get_bb(self):
        if self.size == 2 and self.frame >= 5.0:
            return self.x - 10, self.y - 15, self.x + 15, self.y + 10
        elif self.size == 1 and self.frame >= 5.0:
            return self.x - 20, self.y - 35, self.x + 35, self.y + 20
        else:
            return 0,0,0,0
    def handle_collision(self, group, other):
        pass
