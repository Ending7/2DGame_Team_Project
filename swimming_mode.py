from pico2d import *
import game_world
import game_framework
import gameover_mode
import pause_mode
import title_mode
from swimmer import Swimmer
from key_explain import Keyexplain
from swimmer_stamina import Swimmer_stamina
from swimming_map import Swimming_map



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
    global keyexplain
    global swimmer_stamina

    swimming_map = Swimming_map()
    game_world.add_object(swimming_map, 0)

    swimmer = Swimmer()
    game_world.add_object(swimmer, 2)

    key_explain = Keyexplain()
    game_world.add_object(key_explain, 3)
    swimmer_stamina = Swimmer_stamina()
    game_world.add_object(swimmer_stamina, 4)


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

    # 충돌 상황 등록


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()
    if swimmer.die:
        game_framework.change_mode(gameover_mode)

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
