from pico2d import *

import random
import math
import game_framework
from level3 import running_mode
from level3.behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector
import level3.running_mode

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 5.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Idle']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 11)]

    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0  # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'

        self.tx, self.ty = 1000, 1000
        self.build_behavior_tree()

    def get_bb(self):
        return self.x - 30, self.y - 50, self.x + 30, self.y + 35

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here
        self.bt.run()

    def draw(self):
        if math.cos(self.dir) < 0:
            Zombie.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        pass

    def set_target_location(self, x=None, y=None):
        if not x or not y:
            raise ValueError('위치 지정을 해야 합니다.')
        self.tx, self.ty = x, y
        return BehaviorTree.SUCCESS
        pass

    def distance_less_than(self, x1, y1, x2, y2, r):
        distanc2 = (x1 - x2) ** 2 + (y1 - y2) ** 2
        return distanc2 < (r * PIXEL_PER_METER) ** 2
        pass

    def move_slightly_to(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_slightly_opposite(self, tx, ty):
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.speed = RUN_SPEED_PPS
        self.x -= self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y -= self.speed * math.sin(self.dir) * game_framework.frame_time

    def move_to(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(self.tx, self.ty)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def set_random_location(self):
        self.tx, self.ty = random.randint(100, 1280 - 100), random.randint(50, 450)
        return BehaviorTree.SUCCESS
        pass

    def is_runner_nearby(self, r):
        if self.distance_less_than(running_mode.runner.x, running_mode.runner.y, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def move_to_runner(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_to(running_mode.runner.x, running_mode.runner.y)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def move_opposite_runner(self, r=0.5):
        self.state = 'Walk'
        self.move_slightly_opposite(running_mode.runner.x, running_mode.runner.y)
        if self.distance_less_than(self.tx, self.ty, self.x, self.y, r):
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING

    def is_not_less_than_runners_ball(self):
        if self.ball_count >= running_mode.runner.ball_count:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def less_than_runners_ball(self):
        if self.ball_count < running_mode.runner.ball_count:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.FAIL

    def get_patrol_location(self):
        pass

    def build_behavior_tree(self):
        a1 = Action('set target location', self.set_target_location, 500, 50)  # action node 생성
        a2 = Action('Move to', self.move_to)

        SEQ_move_to_target_location = Sequence('Move to target location', a1, a2)

        a3 = Action('Set random location', self.set_random_location)

        SEQ_wander = Sequence('wander', a3, a2)

        c1 = Condition('플레이어가 근처에 있는가?', self.is_runner_nearby, 7)
        a4 = Action('플레이어에게 이동', self.move_to_runner)

        SEQ_chase_runner = Sequence('플레이어를 추적', c1, a4)


        root = SEL_chase_or_wander = Selector('추적 또는 배회', SEQ_chase_runner, SEQ_wander)

        self.bt = BehaviorTree(root)
        pass
