from pico2d import *
import random
import game_world
import game_framework
import gameover_mode
import pause_mode
import title_mode
from rock import Rock
from player import Player
from bridge import Bridge
from key_explain import Keyexplain
from stamina_bar import Staminabar
from swimming_map import Swimming_map


def spawn_rock():
    global rock_init_time
    global rock_spawn_time

    rock_spawn_time = get_time() - rock_init_time

    if rock_spawn_time >= 0.5:
        rock = Rock(1500, random.randint(580, 580))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('player:rock', None, rock)

        rock = Rock(1500, random.randint(260, 260))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('player:rock', None, rock)

        rock = Rock(1500, random.randint(280, 430))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('player:rock', None, rock)

        rock = Rock(1500, random.randint(440, 560))
        game_world.add_object(rock, 1)
        game_world.add_collision_pair('player:rock', None, rock)

        rock_init_time = get_time()


def player_idle():
    player.dirX = 0
    player.dirY = 0
    player.dir_left, player.dir_right, player.dir_up, player.dir_down = 0, 0, 0, 0
    player.dir_lshift = 0
    swimming_map.dirX = 0
    swimming_map.dirY = 0
    swimming_map.dir_left, swimming_map.dir_right = 0, 0
    player.state_machine.handle_event(('LETS_IDLE', 0))


def create_object():
    global swimming_map
    global bridge
    global player
    global rock
    global keyexplain
    global staminabar

    swimming_map = Swimming_map()
    game_world.add_object(swimming_map, 0)
    bridge = Bridge()
    game_world.add_object(bridge, 1)
    player = Player()
    game_world.add_object(player, 2)

    key_explain = Keyexplain()
    game_world.add_object(key_explain, 3)
    stamina_bar = Staminabar()
    game_world.add_object(stamina_bar, 4)


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
            player.handle_event(event)


def init():
    global swimming_map
    global bridge
    global player
    global rock
    global keyexplain
    global staminabar
    global check_time
    global time_lock
    global rock_init_time

    time_lock = False
    check_time = get_time()
    rock_init_time = get_time()
    # 객체 생성
    create_object()

    # 충돌 상황 등록
    game_world.add_collision_pair('player:rock', player, None)


def finish():
    game_world.remove_all_object('player:rock')
    game_world.clear()
    pass


def update():
    spawn_rock()
    game_world.update()
    game_world.handle_collision()
    if player.die:
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
    player_idle()
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
