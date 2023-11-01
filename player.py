# 이것은 각 상태들을 객체로 구현한 것임.
from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, SDLK_UP, SDLK_DOWN, load_font, \
    get_time
import game_world
import play_mode


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


def time_out(e):
    return e[0] == 'TIME_OUT'


def lets_idle(e):
    return e[0] == 'LETS_IDLE'


# time_out = lambda e : e[0] == 'TIME_OUT'


class Idle:

    @staticmethod
    def enter(player, e):
        player.dir_X = 0
        player.dir_y = 0
        player.dir_left, player.dir_right, player.dir_up, player.dir_down = 0, 0, 0, 0
        print('idle_right:')
        print(player.dir_right)
        print('idle_left:')
        print(player.dir_left)
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = player.frame

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 91, player.action * 79, 90, 79, player.x, player.y, 70, 70)


# 네방향 모두를 스무스하게 움직이게 하려면 경우의수를 따져봐야 한다.
class Run:

    @staticmethod
    def enter(player, e):
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

        elif right_up(e):
            player.dir_right = 0
            player.dirX = 0
            if player.dir_left == 1:
                player.dirX, player.action = -1, 1
            elif player.dir_up == 1:
                player.dirX, player.dirY, player.action = 0, 1, 1
            elif player.dir_down == 1:
                player.dirX, player.dirY, player.action = 0, -1, 1

        elif left_up(e):
            player.dir_left = 0
            player.dirX = 0
            if player.dir_right == 1:
                player.dirX, player.action = 1, 1
            elif player.dir_up == 1:
                player.dirX, player.dirY, player.action = 0, 1, 1
            elif player.dir_down == 1:
                player.dirX, player.dirY, player.action = 0, -1, 1

        elif up_up(e):
            player.dir_up = 0
            player.dirY = 0
            if player.dir_down == 1:
                player.dirY, player.action = -1, 1
            elif player.dir_right == 1:
                player.dirX, player.dirY, player.action = 1, 0, 1
            elif player.dir_left == 1:
                player.dirX, player.dirY, player.action = -1, 0, 1

        elif down_up(e):
            player.dir_down = 0
            player.dirY = 0
            if player.dir_up == 1:
                player.dirY, player.action = 1, 1
            elif player.dir_right == 1:
                player.dirX, player.dirY, player.action = 1, 0, 1
            elif player.dir_left == 1:
                player.dirX, player.dirY, player.action = -1, 0, 1

        if player.dir_left == 0 and player.dir_right == 0 and player.dir_up == 0 and player.dir_down == 0:
            player.state_machine.handle_event(('LETS_IDLE', 0))

        print('run_right, left:', player.dir_right, player.dir_left)
        print('run_up, down:', player.dir_up, player.dir_down)
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        player.frame = (player.frame + 1) % 12
        player.x += player.dirX * 3.0
        player.y += player.dirY * 3.0
        if player.x <= 0 + 32:
            player.x = 0 + 32
        if player.x >= 1440 - 74:
            player.x = 1440 - 74
        if player.y <= 280:
            player.y = 280
        if player.y >= 600:
            player.y = 600

        pass

    @staticmethod
    def draw(player):
        player.image.clip_draw(player.frame * 91, player.action * 79, 90, 79, player.x, player.y, 70, 70)


class StateMachine:
    def __init__(self, player):
        self.player = player
        self.cur_state = Idle
        self.transitions = {
            Idle: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run, up_up: Run,
                   down_down: Run, down_up: Run},
            Run: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, up_down: Run,
                  up_up: Run, down_down: Run, down_up: Run, lets_idle: Idle}
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
        self.dir_left, self.dir_right, self.dir_up, self.dir_down = 0, 0, 0, 0
        self.image = load_image('cycling.png')
        self.font = load_font('ENCR10B.TTF', 32)
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if play_mode.timelock == False:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {get_time()-play_mode.checktime:.2f})', (255, 0, 0))
        elif play_mode.timelock == True:
            self.font.draw(1400 / 2 - 100, 780, f'(Time: {play_mode.pausetime - play_mode.checktime:.2f})', (255, 0, 0))
        pass
