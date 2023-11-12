from pico2d import *
import random
import game_world
import game_framework
import gameover_mode
import pause_mode
from level2 import swimming_mode
import title_mode
from level1.rock import Rock
from level1.cycler import Cycler
from level1.cycling_map import Cycling_map
from level1.bridge import Bridge
from key_explain import Keyexplain
from level1.cycler_stamina import Cycler_stamina


def spawn_rock():
    global rock_init_time
    global rock_spawn_time

    rock_spawn_time = get_time() - rock_init_time

    if rock_spawn_time >= 0.5:
        rock = Rock(1500, random.randint(580, 580))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('cycler:rock', None, rock)

        rock = Rock(1500, random.randint(260, 260))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('cycler:rock', None, rock)

        rock = Rock(1500, random.randint(280, 430))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('cycler:rock', None, rock)

        rock = Rock(1500, random.randint(440, 560))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('cycler:rock', None, rock)

        rock_init_time = get_time()


def cycler_idle():
    cycler.dirX = 0
    cycler.dirY = 0
    cycler.dir_left, cycler.dir_right, cycler.dir_up, cycler.dir_down = 0, 0, 0, 0
    cycler.dir_lshift = 0
    cycling_map.dirX = 0
    cycling_map.dirY = 0
    cycling_map.dir_left, cycling_map.dir_right = 0, 0
    cycler.state_machine.handle_event(('LETS_IDLE', 0))


def create_object():
    global cycling_map
    global bridge
    global cycler
    global rock
    global keyexplain
    global cycler_stamina

    cycling_map = Cycling_map()
    game_world.add_object(cycling_map, 0)
    bridge = Bridge()
    game_world.add_object(bridge, 1)
    cycler = Cycler()
    game_world.add_object(cycler, 2)

    key_explain = Keyexplain()
    game_world.add_object(key_explain, 3)
    cycler_stamina = Cycler_stamina()
    game_world.add_object(cycler_stamina, 4)


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
            cycler.handle_event(event)


def init():
    global cycling_map
    global bridge
    global cycler
    global rock
    global keyexplain
    global cycler_stamina
    global check_time
    global time_lock
    global rock_init_time

    time_lock = False
    check_time = get_time()
    rock_init_time = get_time()
    # 객체 생성
    create_object()

    # 충돌 상황 등록
    game_world.add_collision_pair('cycler:rock', cycler, None)


def finish():
    game_world.remove_all_object('cycler:rock')
    game_world.clear()
    pass


def update():
    spawn_rock()
    game_world.update()
    game_world.handle_collision()
    if cycler.die:
        game_framework.change_mode(gameover_mode)
    if cycler.success:
        game_framework.change_mode(swimming_mode)

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
    cycler_idle()
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