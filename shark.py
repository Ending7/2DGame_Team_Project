import random

from pico2d import load_image, draw_rectangle

import game_framework
import swimming_mode

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 6
FRAMES_PER_TIME = ACTION_PER_TIME * FRAMES_PER_ACTION

class Shark:
    def __init__(self, sharkX, sharkY, size):
        self.image = load_image('./resource/shark.png')
        self.action = 0
        self.frame = 0
        self.x = sharkX
        self.y = sharkY
        self.size = size
        self.speed = random.randint(1, 10)

    def draw(self):
        if self.action == 0:
            self.image.clip_draw(int(self.frame) * 56, self.action * 90, 56, 90, self.x, self.y, 95/self.size, 95/self.size)
            draw_rectangle(*self.get_bb())
        elif self.action == 1:
            self.image.clip_draw(int(self.frame) *56 , self.action * 90, 56, 90, self.x, self.y, 95/self.size, 95/self.size)
            draw_rectangle(*self.get_bb())


    def update(self):
        if swimming_mode.time_lock == False:
            self.frame = (self.frame + FRAMES_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
            if self.action == 0:
                self.y -= 1 * 10 * game_framework.frame_time * self.speed
            elif self.action == 1:
                self.y += 1 * 10 * game_framework.frame_time * self.speed

            if self.y <= 50:
                self.action = 1
            elif self.y >= 450:
                self.action = 0


    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_collision(self, group, other):
        pass
