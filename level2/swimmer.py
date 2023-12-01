# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, load_font, \
    get_time, SDLK_LSHIFT, draw_rectangle
import game_framework
import game_world
from level1 import cycling_mode
from level2 import swimming_mode

PIXEL_PER_METER = (10.0 / 0.3)  # m당 몇 픽셀이냐 / 10px에 30cm. 10px에 0.3m.
RUN_SPEED_KMPH = 20.0  # Km / Hour 한 시간에 마라톤 선수가 대략 20km를 달린다.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 1분에 몇m 움직였는지
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 1초에 몇m 움직였는지 알아야 한다.
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 초당 몇 픽셀만큼 움직이는지. 미터당 비례하는 픽셀 수를 알았으니, 1초에 움직인 m * 픽셀수를 곱해주면 나온다.

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 2.0이게 뭘 하는 것? 프레임 속력2 1초에 2번
FRAME_PER_ACTION = 6


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


def any_key_down(swimmer, e):
    if right_down(e):
        swimmer.dir_right = 1
        swimmer.dirX, swimmer.action = 1, 1
    elif left_down(e):
        swimmer.dir_left = 1
        swimmer.dirX, swimmer.action = -1, 1
    elif up_down(e):
        swimmer.dir_up = 1
        swimmer.dirY, swimmer.action = 1, 1
    elif down_down(e):
        swimmer.dir_down = 1
        swimmer.dirY, swimmer.action = -1, 1
    elif lshift_down(e):
        swimmer.dir_shift = 1


def right_key_up(swimmer, e):
    if right_up(e):
        swimmer.dir_right = 0
        swimmer.dirX = 0
        if swimmer.dir_left == 1:
            swimmer.dirX, swimmer.action = -1, 1
        elif swimmer.dir_up == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 0, 1, 1
        elif swimmer.dir_down == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 0, -1, 1


def left_key_up(swimmer, e):
    if left_up(e):
        swimmer.dir_left = 0
        swimmer.dirX = 0
        if swimmer.dir_right == 1:
            swimmer.dirX, swimmer.action = 1, 1
        elif swimmer.dir_up == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 0, 1, 1
        elif swimmer.dir_down == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 0, -1, 1


def up_key_up(swimmer, e):
    if up_up(e):
        swimmer.dir_up = 0
        swimmer.dirY = 0
        if swimmer.dir_down == 1:
            swimmer.dirY, swimmer.action = -1, 1
        elif swimmer.dir_right == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 1, 0, 1
        elif swimmer.dir_left == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = -1, 0, 1


def down_key_up(swimmer, e):
    if down_up(e):
        swimmer.dir_down = 0
        swimmer.dirY = 0
        if swimmer.dir_up == 1:
            swimmer.dirY, swimmer.action = 1, 1
        elif swimmer.dir_right == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = 1, 0, 1
        elif swimmer.dir_left == 1:
            swimmer.dirX, swimmer.dirY, swimmer.action = -1, 0, 1


def use_stamina(swimmer):
    if swimmer.dir_shift == 1 and swimming_mode.time_lock == False:
        swimmer.speed = 2
        if swimmer.stamina >= 0:
            swimmer.stamina -= 1 * RUN_SPEED_PPS * game_framework.frame_time
    elif swimmer.dir_shift == 0 and swimming_mode.time_lock == False:
        swimmer.speed = 1
        if swimmer.stamina < 65:
            swimmer.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if swimmer.stamina <= 0:
        swimmer.stamina_lock = True
    elif swimmer.stamina >= 65:
        swimmer.stamina_lock = False


def swimmer_move(swimmer):
    if swimming_mode.time_lock == False and swimmer.stamina_lock == False:
        swimmer.frame = (swimmer.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        swimmer.x += swimmer.dirX * RUN_SPEED_PPS * game_framework.frame_time * swimmer.speed * swimmer.swirl_speed * swimmer.item_speed
        swimmer.y += swimmer.dirY * RUN_SPEED_PPS * game_framework.frame_time * swimmer.speed * swimmer.swirl_speed * swimmer.item_speed
    if swimmer.x <= 0 + 32:
        swimmer.x = 0 + 32
    if swimmer.x >= 1440 - 74:
        swimmer.x = 1440 - 74
    if swimmer.y <= 35:
        swimmer.y = 35
    if swimmer.y >= 450:
        swimmer.y = 450


def swimmer_move_stop(swimmer):
    swimmer.dir_X = 0
    swimmer.dir_y = 0
    swimmer.dir_shift = 0
    swimmer.dir_left, swimmer.dir_right, swimmer.dir_up, swimmer.dir_down = 0, 0, 0, 0
    swimmer.speed = 0


def debug(swimmer):
    print('right:')
    print(swimmer.dir_right)
    print('left:')
    print(swimmer.dir_left)
    print('up:')
    print(swimmer.dir_up)
    print('down:')
    print(swimmer.dir_down)


def stamina_recovery(swimmer):
    if swimmer.stamina < 65 and swimming_mode.time_lock == False:
        swimmer.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if swimmer.stamina_lock == True and swimmer.stamina >= 65:
        swimmer.stamina_lock = False


class Idle:
    @staticmethod
    def enter(swimmer, e):
        swimmer.frame = 0
        swimmer.action = 4
        swimmer_move_stop(swimmer)
        debug(swimmer)
        pass

    @staticmethod
    def exit(swimmer, e):
        pass

    @staticmethod
    def do(swimmer):
        swimmer.frame = (swimmer.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 6
        stamina_recovery(swimmer)

    @staticmethod
    def draw(swimmer):
        swimmer.image.clip_draw(int(swimmer.frame) * 220, swimmer.action * 240, 220, 240, swimmer.x, swimmer.y, 95, 95)


# 네방향 모두를 스무스하게 움직이게 하려면 경우의수를 따져봐야 한다.
class Run:

    @staticmethod
    def enter(swimmer, e):
        swimmer.frame = 0
        swimmer.action = 1
        any_key_down(swimmer, e)
        right_key_up(swimmer, e)
        left_key_up(swimmer, e)
        up_key_up(swimmer, e)
        down_key_up(swimmer, e)
        if lshift_up(e):
            swimmer.dir_shift = 0
        if swimmer.dir_left == 0 and swimmer.dir_right == 0 and swimmer.dir_up == 0 and swimmer.dir_down == 0:
            swimmer.state_machine.handle_event(('LETS_IDLE', 0))
        debug(swimmer)
        pass

    @staticmethod
    def exit(swimmer, e):
        pass

    @staticmethod
    def do(swimmer):
        use_stamina(swimmer)
        swimmer_move(swimmer)
        if swimmer.x >= 1350:
            swimmer.success = True
            game_world.records.insert(1,get_time() - swimming_mode.check_time)
        pass

    @staticmethod
    def draw(swimmer):
        swimmer.image.clip_draw(int(swimmer.frame) * 224, swimmer.action * 260, 224, 260, swimmer.x, swimmer.y, 95, 100)


class StateMachine:
    def __init__(self, swimmer):
        self.swimmer = swimmer
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lshift_down: Run, lshift_up: Run, lets_idle: Idle}
        }

    def start(self):
        self.cur_state.enter(self.swimmer, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.swimmer)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.swimmer, e)
                self.cur_state = next_state
                self.cur_state.enter(self.swimmer, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.swimmer)


class Swimmer:
    def __init__(self):
        self.x, self.y = 50, 420
        self.frame = 0
        self.action = 0
        self.dirX = 0
        self.dirY = 0
        self.speed = 1.0
        self.item_speed = 1.0
        self.swirl_speed = 1.0
        self.stamina = 65
        self.success = False
        self.die = False
        self.stamina_lock = False
        self.dir_left, self.dir_right, self.dir_up, self.dir_down, self.dir_shift = 0, 0, 0, 0, 0
        self.image = load_image('./resource/swimmer.png')
        self.font = load_font('./resource/ENCR10B.TTF', 32)
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.speed_mode = False

    def update(self):

        if self.speed_mode == True:
            self.item_speed = 2.0
        else:
            self.item_speed = 1.0
        self.state_machine.update()
        self.swirl_speed = 1.0
    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if swimming_mode.time_lock == False:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {get_time() - swimming_mode.check_time:.2f})', (255, 0, 0))
        elif swimming_mode.time_lock == True:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {swimming_mode.pause_time - swimming_mode.check_time:.2f})',
                           (255, 0, 0))
        if self.stamina_lock == True:
            self.font.draw(self.x - 100, self.y + 40, f'Now Groggy...', (0, 0, 255))

        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 25, self.y-15, self.x + 40, self.y + 10

    def handle_collision(self, group, other):
        if group == 'swimmer:shark':
            game_world.delete_record_time()
            self.die = True
        if group == 'swimmer:swirl':
            self.swirl_speed = 0.3
