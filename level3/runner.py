# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, load_font, \
    get_time, SDLK_LSHIFT, draw_rectangle
import game_framework
import game_world
from level3 import running_mode

PIXEL_PER_METER = (10.0 / 0.3)  # m당 몇 픽셀이냐 / 10px에 30cm. 10px에 0.3m.
RUN_SPEED_KMPH = 20.0  # Km / Hour 한 시간에 마라톤 선수가 대략 20km를 달린다.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 1분에 몇m 움직였는지
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 1초에 몇m 움직였는지 알아야 한다.
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 초당 몇 픽셀만큼 움직이는지. 미터당 비례하는 픽셀 수를 알았으니, 1초에 움직인 m * 픽셀수를 곱해주면 나온다.

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 2.0이게 뭘 하는 것? 프레임 속력2 1초에 2번
FRAME_PER_ACTION = 10


# state event check
# ( state event type, event value )
def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def up_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def up_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def down_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def down_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def lshift_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LSHIFT


def lshift_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LSHIFT


def time_out(e):
    return e[0] == 'TIME_OUT'


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


def any_key_down(runner, e):
    if right_down(e):
        runner.dir_right = 1
        runner.dirX, runner.action = 1, 1
    elif left_down(e):
        runner.dir_left = 1
        runner.dirX, runner.action = -1, 1
    elif up_down(e):
        runner.dir_up = 1
        runner.dirY, runner.action = 1, 1
    elif down_down(e):
        runner.dir_down = 1
        runner.dirY, runner.action = -1, 1
    elif lshift_down(e):
        runner.dir_shift = 1


def right_key_up(runner, e):
    if right_up(e):
        runner.dir_right = 0
        runner.dirX = 0
        if runner.dir_left == 1:
            runner.dirX, runner.action = -1, 1
        elif runner.dir_up == 1:
            runner.dirX, runner.dirY, runner.action = 0, 1, 1
        elif runner.dir_down == 1:
            runner.dirX, runner.dirY, runner.action = 0, -1, 1


def left_key_up(runner, e):
    if left_up(e):
        runner.dir_left = 0
        runner.dirX = 0
        if runner.dir_right == 1:
            runner.dirX, runner.action = 1, 1
        elif runner.dir_up == 1:
            runner.dirX, runner.dirY, runner.action = 0, 1, 1
        elif runner.dir_down == 1:
            runner.dirX, runner.dirY, runner.action = 0, -1, 1


def up_key_up(runner, e):
    if up_up(e):
        runner.dir_up = 0
        runner.dirY = 0
        if runner.dir_down == 1:
            runner.dirY, runner.action = -1, 1
        elif runner.dir_right == 1:
            runner.dirX, runner.dirY, runner.action = 1, 0, 1
        elif runner.dir_left == 1:
            runner.dirX, runner.dirY, runner.action = -1, 0, 1


def down_key_up(runner, e):
    if down_up(e):
        runner.dir_down = 0
        runner.dirY = 0
        if runner.dir_up == 1:
            runner.dirY, runner.action = 1, 1
        elif runner.dir_right == 1:
            runner.dirX, runner.dirY, runner.action = 1, 0, 1
        elif runner.dir_left == 1:
            runner.dirX, runner.dirY, runner.action = -1, 0, 1


def use_stamina(runner):
    if runner.dir_shift == 1 and running_mode.time_lock == False:
        runner.speed = 2
        if runner.stamina >= 0:
            runner.stamina -= 1 * RUN_SPEED_PPS * game_framework.frame_time
    elif runner.dir_shift == 0 and running_mode.time_lock == False:
        runner.speed = 1
        if runner.stamina < 65:
            runner.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if runner.stamina <= 0:
        runner.stamina_lock = True
    elif runner.stamina >= 65:
        runner.stamina_lock = False


def runner_move(runner):
    if running_mode.time_lock == False and runner.stamina_lock == False:
        runner.frame = (runner.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 10
        runner.x += runner.dirX * RUN_SPEED_PPS * game_framework.frame_time * runner.speed* runner.item_speed
        runner.y += runner.dirY * RUN_SPEED_PPS * game_framework.frame_time * runner.speed* runner.item_speed
    if runner.x <= 0 + 32:
        runner.x = 0 + 32
    if runner.x >= 1440 - 74:
        runner.x = 1440 - 74
    if runner.y <= 35:
        runner.y = 35
    if runner.y >= 450:
        runner.y = 450


def runner_move_stop(runner):
    runner.dir_X = 0
    runner.dir_y = 0
    runner.dir_shift = 0
    runner.dir_left, runner.dir_right, runner.dir_up, runner.dir_down = 0, 0, 0, 0
    runner.speed = 0


def debug(runner):
    print('right:')
    print(runner.dir_right)
    print('left:')
    print(runner.dir_left)
    print('up:')
    print(runner.dir_up)
    print('down:')
    print(runner.dir_down)


def stamina_recovery(runner):
    if runner.stamina < 65 and running_mode.time_lock == False:
        runner.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if runner.stamina_lock == True and runner.stamina >= 65:
        runner.stamina_lock = False


class Idle:
    @staticmethod
    def enter(runner, e):
        runner.action = 1
        runner.frame = 0
        runner_move_stop(runner)
        debug(runner)
        pass

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner):
        runner.frame = 0
        runner.action = 1
        stamina_recovery(runner)

    @staticmethod
    def draw(runner):
        runner.image.clip_draw(int(runner.frame) * 47, 1 * 59, 47, 59, runner.x, runner.y, 100,100)


# 네방향 모두를 스무스하게 움직이게 하려면 경우의수를 따져봐야 한다.
class Run:

    @staticmethod
    def enter(runner, e):
        runner.frame = runner.frame
        runner.action = 0
        any_key_down(runner, e)
        right_key_up(runner, e)
        left_key_up(runner, e)
        up_key_up(runner, e)
        down_key_up(runner, e)
        if lshift_up(e):
            runner.dir_shift = 0
        if runner.dir_left == 0 and runner.dir_right == 0 and runner.dir_up == 0 and runner.dir_down == 0:
            runner.state_machine.handle_event(('LETS_IDLE', 0))
        debug(runner)
        pass

    @staticmethod
    def exit(runner, e):
        pass

    @staticmethod
    def do(runner, runner_mode=None):
        runner.action = 0
        use_stamina(runner)
        runner_move(runner)
        if runner.x >= 1350:
            runner.success = True
            game_world.records.insert(2,get_time() - running_mode.check_time)
            game_world.records.insert(3, (game_world.records[0] + game_world.records[1] + game_world.records[2]))
            game_world.confirm_record_time()
        pass

    @staticmethod
    def draw(runner):
        runner.image.clip_draw(int(runner.frame) * 47, 0 * 59, 47, 59, runner.x, runner.y, 100, 100)


class StateMachine:
    def __init__(self, runner):
        self.runner = runner
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lshift_down: Run, lshift_up: Run, lets_idle: Idle}
        }

    def start(self):
        self.cur_state.enter(self.runner, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.runner)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.runner, e)
                self.cur_state = next_state
                self.cur_state.enter(self.runner, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.runner)


class Runner:
    def __init__(self):
        self.x, self.y = 50, 420
        self.frame = 0
        self.action = 0
        self.dirX = 0
        self.dirY = 0
        self.speed = 1
        self.item_speed = 1
        self.stamina = 65
        self.success = False
        self.die = False
        self.stamina_lock = False
        self.dir_left, self.dir_right, self.dir_up, self.dir_down, self.dir_shift = 0, 0, 0, 0, 0
        self.image = load_image('./resource/runner.png')
        self.font = load_font('./resource/ENCR10B.TTF', 32)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.speed_mode = False
        self.speed_time = 0
        self.invisibility_mode = False
        self.invisibility_time = 0

    def update(self):
        if self.speed_mode == True:
            self.item_speed = 2.0
            self.speed_time += game_framework.frame_time
            if self.speed_time >= 2.0:
                self.speed_time = 0
                self.item_speed = 1.0
                self.speed_mode = False

        if self.invisibility_mode == True:
            self.invisibility_time += game_framework.frame_time
            if self.invisibility_time >= 2.0:
                self.invisibility_time = 0
                self.invisibility_mode = False
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if running_mode.time_lock == False:
            self.font.draw(1400 / 2 - 120, 740, f'(Time: {get_time() - running_mode.check_time:.2f})', (255, 0, 0))
        elif running_mode.time_lock == True:
            self.font.draw(1400 / 2 - 120, 740, f'(Time: {running_mode.pause_time - running_mode.check_time:.2f})',
                           (255, 0, 0))
        if self.speed_mode == True:
            self.font.draw(self.x - 170, self.y + 50, f'(speed_time: {2.0 - self.speed_time:.2f})', (0, 0, 255))
        if self.invisibility_mode == True:
            self.font.draw(self.x - 230, self.y + 50, f'(invisibility_time: {2.0 - self.invisibility_time:.2f})',(0, 255, 0))
        if self.stamina_lock == True:
            self.font.draw(self.x - 100, self.y + 40, f'Now Groggy...', (0, 0, 255))

        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        if self.action == 1:
            return self.x - 15, self.y-45, self.x + 15, self.y - 35
        elif self.action == 0:
            return self.x - 30, self.y-45, self.x + 30, self.y - 35

    def handle_collision(self, group, other):
        if self.invisibility_mode == False:
            if group == 'runner:splinter':
                game_world.delete_record_time()
                self.die = True
            if group == 'runner:zombie':
                game_world.delete_record_time()
                self.die = True
