# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, load_font, \
    get_time, SDLK_LSHIFT, draw_rectangle
import game_framework
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)  # m당 몇 픽셀이냐 / 10px에 30cm. 10px에 0.3m.
RUN_SPEED_KMPH = 20.0  # Km / Hour 한 시간에 마라톤 선수가 대략 20km를 달린다.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 1분에 몇m 움직였는지
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 1초에 몇m 움직였는지 알아야 한다.
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 초당 몇 픽셀만큼 움직이는지. 미터당 비례하는 픽셀 수를 알았으니, 1초에 움직인 m * 픽셀수를 곱해주면 나온다.

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION  # 2.0이게 뭘 하는 것? 프레임 속력2 1초에 2번
FRAME_PER_ACTION = 12


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


def any_key_down(player, e):
    if right_down(e):
        player.dir_right = 1
        player.dirX, player.action = 1, 1
    elif left_down(e):
        player.dir_left = 1
        player.dirX, player.action = -1, 1
    elif up_down(e):
        player.dir_up = 1
        player.dirY, player.action = 1, 1
    elif down_down(e):
        player.dir_down = 1
        player.dirY, player.action = -1, 1
    elif lshift_down(e):
        player.dir_shift = 1


def right_key_up(player, e):
    if right_up(e):
        player.dir_right = 0
        player.dirX = 0
        if player.dir_left == 1:
            player.dirX, player.action = -1, 1
        elif player.dir_up == 1:
            player.dirX, player.dirY, player.action = 0, 1, 1
        elif player.dir_down == 1:
            player.dirX, player.dirY, player.action = 0, -1, 1


def left_key_up(player, e):
    if left_up(e):
        player.dir_left = 0
        player.dirX = 0
        if player.dir_right == 1:
            player.dirX, player.action = 1, 1
        elif player.dir_up == 1:
            player.dirX, player.dirY, player.action = 0, 1, 1
        elif player.dir_down == 1:
            player.dirX, player.dirY, player.action = 0, -1, 1


def up_key_up(player, e):
    if up_up(e):
        player.dir_up = 0
        player.dirY = 0
        if player.dir_down == 1:
            player.dirY, player.action = -1, 1
        elif player.dir_right == 1:
            player.dirX, player.dirY, player.action = 1, 0, 1
        elif player.dir_left == 1:
            player.dirX, player.dirY, player.action = -1, 0, 1


def down_key_up(player, e):
    if down_up(e):
        player.dir_down = 0
        player.dirY = 0
        if player.dir_up == 1:
            player.dirY, player.action = 1, 1
        elif player.dir_right == 1:
            player.dirX, player.dirY, player.action = 1, 0, 1
        elif player.dir_left == 1:
            player.dirX, player.dirY, player.action = -1, 0, 1


def use_stamina(player):
    if player.dir_shift == 1 and play_mode.time_lock == False:
        player.speed = 2
        if player.stamina >= 0:
            player.stamina -= 1 * RUN_SPEED_PPS * game_framework.frame_time
    elif player.dir_shift == 0 and play_mode.time_lock == False:
        player.speed = 1
        if player.stamina < 65:
            player.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if player.stamina <= 0:
        player.stamina_lock = True
    elif player.stamina >= 65:
        player.stamina_lock = False


def player_move(player):
    if play_mode.time_lock == False and player.stamina_lock == False:
        player.frame = (player.frame + FRAME_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 12
        player.x += player.dirX * RUN_SPEED_PPS * game_framework.frame_time * player.speed
        player.y += player.dirY * RUN_SPEED_PPS * game_framework.frame_time * player.speed
    if player.x <= 0 + 32:
        player.x = 0 + 32
    if player.x >= 1440 - 74:
        player.x = 1440 - 74
    if player.y <= 280:
        player.y = 280
    if player.y >= 600:
        player.y = 600


def player_move_stop(player):
    player.dir_X = 0
    player.dir_y = 0
    player.dir_shift = 0
    player.dir_left, player.dir_right, player.dir_up, player.dir_down = 0, 0, 0, 0
    player.speed = 0

def debug(player):
    print('right:')
    print(player.dir_right)
    print('left:')
    print(player.dir_left)
    print('up:')
    print(player.dir_up)
    print('down:')
    print(player.dir_down)

def stamina_recovery(player):
    if player.stamina < 65 and play_mode.time_lock == False:
        player.stamina += 1 * RUN_SPEED_PPS * game_framework.frame_time / 2
    if player.stamina_lock == True and player.stamina >= 65:
        player.stamina_lock = False

class Idle:
    @staticmethod
    def enter(player, e):
        player_move_stop(player)
        debug(player)
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = player.frame
        stamina_recovery(player)

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 91, player.action * 79, 90, 79, player.x, player.y, 70, 70)


# 네방향 모두를 스무스하게 움직이게 하려면 경우의수를 따져봐야 한다.
class Run:

    @staticmethod
    def enter(player, e):
        any_key_down(player, e)
        right_key_up(player, e)
        left_key_up(player, e)
        up_key_up(player, e)
        down_key_up(player, e)
        if lshift_up(e):
            player.dir_shift = 0
        if player.dir_left == 0 and player.dir_right == 0 and player.dir_up == 0 and player.dir_down == 0:
            player.state_machine.handle_event(('LETS_IDLE', 0))
        debug(player)
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        use_stamina(player)
        player_move(player)
        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(int(player.frame) * 91, player.action * 79, 90, 79, player.x, player.y, 70, 70)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lshift_down: Run, lshift_up: Run, lets_idle: Idle}
        }

    def start(self):
        self.cur_state.enter(self.player, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.player)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.player, e)
                self.cur_state = next_state
                self.cur_state.enter(self.player, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.player)


class Player:
    def __init__(self):
        self.x, self.y = 50, 420
        self.frame = 0
        self.action = 0
        self.dirX = 0
        self.dirY = 0
        self.speed = 1
        self.stamina = 65
        self.stamina_lock = False
        self.dir_left, self.dir_right, self.dir_up, self.dir_down, self.dir_shift = 0, 0, 0, 0, 0
        self.image = load_image('./resource/cycling.png')
        self.font = load_font('./resource/ENCR10B.TTF', 32)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if play_mode.time_lock == False:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {get_time() - play_mode.check_time:.2f})', (255, 0, 0))
        elif play_mode.time_lock == True:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {play_mode.pause_time - play_mode.check_time:.2f})',
                           (255, 0, 0))
        if self.stamina_lock == True:
            self.font.draw(self.x - 100, self.y + 40, f'Now Groggy...', (0, 0, 255))

        draw_rectangle(*self.get_bb())
        pass

    def get_bb(self):
        return self.x - 30, self.y - 35, self.x + 30, self.y - 30

