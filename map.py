from pico2d import load_image
from pico2d import SDL_KEYDOWN, SDL_KEYUP, SDLK_LEFT, SDLK_RIGHT

import game_framework

PIXEL_PER_METER = (10.0 / 0.3) # m당 몇 픽셀이냐 / 10px에 30cm. 10px에 0.3m.
RUN_SPEED_KMPH = 10.0 # Km / Hour 한 시간에 마라톤 선수가 대략 20km를 달린다.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0) # 1분에 몇m 움직였는지
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0) #1초에 몇m 움직였는지 알아야 한다.
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER) #초당 몇 픽셀만큼 움직이는지. 미터당 비례하는 픽셀 수를 알았으니, 1초에 움직인 m * 픽셀수를 곱해주면 나온다.

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


class Idle:

    @staticmethod
    def enter(map, e):
        map.dir_X = 0
        map.dir_y = 0
        pass

    @staticmethod
    def exit(map, e):
        pass

    @staticmethod
    def do(map):
        pass

    @staticmethod
    def draw(map):
        map.image.draw(2000 / 1000 + 950 + map.x, 800 / 2)


class Move:
    @staticmethod
    def enter(map, e):
        if right_down(e):
            map.dir_right = 1
            map.dirX = 1
        elif left_down(e):
            map.dir_left = 1
            map.dirX = -1
        elif right_up(e):
            map.dir_right = 0
            map.dirX = 0
            if map.dir_left == 1:
                map.dirX = -1
        elif left_up(e):
            map.dir_left = 0
            map.dirX = 0
            if map.dir_right == 1:
                map.dirX = 1

        if map.dir_left == 0 and map.dir_right == 0:
            map.state_machine.handle_event(('LETS_IDLE', 0))

    @staticmethod
    def exit(map, e):
        pass

    @staticmethod
    def do(map):
        map.x -= map.dirX * RUN_SPEED_PPS * game_framework.frame_time
        if map.x >= 45:
            map.x = 45
        elif map.x <= -500:
            map.x = -500
    @staticmethod
    def draw(map):
        map.image.draw(2000 / 1000 + 950 + map.x, 800 / 2)


class StateMachine:
    def __init__(self, map):
        self.map = map
        self.cur_state = Move
        self.transitions = {
            Idle: {right_down: Move, left_down: Move, right_up: Move, left_up: Move},
            Move: {right_down: Move, left_down: Move, right_up: Move, left_up: Move, lets_idle: Idle}
        }

    def start(self):
        self.cur_state.enter(self.map, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.map)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.map, e)
                self.cur_state = next_state
                self.cur_state.enter(self.map, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.map)


class Map:
    def __init__(self):
        self.x, self.y = 0, 0
        self.dirX = 0
        self.dirY = 0
        self.dir_left, self.dir_right = 0, 0
        self.image = load_image('./resource/map1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
