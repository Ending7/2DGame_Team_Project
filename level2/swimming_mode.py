from pico2d import *
import random
import game_world
import game_framework
import gameover_mode
import pause_mode
import title_mode
from level2.shark import Shark
from level2.swimmer import Swimmer
from key_explain import Keyexplain
from level2.swimmer_stamina import Swimmer_stamina
from level2.swimming_map import Swimming_map
from level2.swirl import Swirl
from level3 import running_mode


def swimmer_idle():
    swimmer.dirX = 0
    swimmer.dirY = 0
    swimmer.dir_left, swimmer.dir_right, swimmer.dir_up, swimmer.dir_down = 0, 0, 0, 0
    swimmer.dir_lshift = 0
    swimming_map.dirX = 0
    swimming_map.dirY = 0
    swimming_map.dir_left, swimming_map.dir_right = 0, 0
    swimmer.state_machine.handle_event(('LETS_IDLE', 0))


def create_object():
    global swimming_map
    global swimmer
    global sharks
    global keyexplain
    global swimmer_stamina

    swimming_map = Swimming_map()
    game_world.add_object(swimming_map, 0)

    swimmer = Swimmer()
    game_world.add_object(swimmer, 2)
    game_world.add_collision_pair('swimmer:shark', swimmer, None)
    game_world.add_collision_pair('swimmer:swirl', swimmer, None)

    key_explain = Keyexplain()
    game_world.add_object(key_explain, 3)
    swimmer_stamina = Swimmer_stamina()
    game_world.add_object(swimmer_stamina, 4)

def create_shark():
    # sharks = [Shark(random.randint(200,1200),random.randint(0,500),random.randint(1,2)) for _ in range(25)]
    sharks = [Shark(random.randint(150, 150), random.randint(0, 500), random.randint(1, 1)) for _ in range(5)]
    sharks += [Shark(random.randint(290, 290), random.randint(0, 500), random.randint(2, 2)) for _ in range(3)]
    sharks += [Shark(random.randint(420, 420), random.randint(0, 500), random.randint(2, 2)) for _ in range(3)]
    sharks += [Shark(random.randint(550, 550), random.randint(0, 500), random.randint(1, 1)) for _ in range(5)]
    sharks += [Shark(random.randint(730, 730), random.randint(0, 500), random.randint(2, 2)) for _ in range(3)]
    sharks += [Shark(random.randint(880, 880), random.randint(0, 500), random.randint(1, 1)) for _ in range(5)]
    sharks += [Shark(random.randint(1030, 1030), random.randint(0, 500), random.randint(2, 2)) for _ in range(3)]
    sharks += [Shark(random.randint(1160, 1160), random.randint(0, 500), random.randint(2, 2)) for _ in range(3)]
    sharks += [Shark(random.randint(1300, 1300), random.randint(0, 500), random.randint(1, 1)) for _ in range(5)]
    game_world.add_objects(sharks, 1)

    for shark in sharks:
        game_world.add_collision_pair('swimmer:shark', None, shark)
def create_swirl():
    swirls = []
    swirls.append(Swirl(230, 50, 2))
    swirls.append(Swirl(355, 415, 2))
    swirls.append(Swirl(480, 50, 2))
    swirls.append(Swirl(730, 250, 1))
    swirls.append(Swirl(960, 415, 2))
    swirls.append(Swirl(1100, 50, 2))
    swirls.append(Swirl(1225, 415, 2))

    for swirl in swirls:
        game_world.add_object(swirl, 0)
        game_world.add_collision_pair('swimmer:swirl', None, swirl)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(pause_mode)
        else:
            swimmer.handle_event(event)


def init():
    global swimming_map
    global bridge
    global swimmer
    global keyexplain
    global swimmer_stamina
    global check_time
    global time_lock

    time_lock = False
    check_time = get_time()
    # 객체 생성
    create_object()
    create_shark()
    create_swirl()

def finish():
    game_world.remove_all_object('swimmer:shark')
    game_world.remove_all_object('swimmer:swirl')
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()
    if swimmer.die:
        game_framework.change_mode(gameover_mode)
    if swimmer.success:
        game_framework.change_mode(running_mode)


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    global pause_time
    global check_time
    global time_lock
    time_lock = True
    pause_time = get_time()
    swimmer_idle()
    pass


def resume():
    global pause_time
    global resume_time
    global check_time
    global time_lock

    time_lock = False
    resume_time = get_time()
    check_time += resume_time - pause_time
    pass
