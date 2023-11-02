from pico2d import *
import game_world
import game_framework
import pause_mode
import title_mode
from player import Player
from map import Map
from bridge import Bridge
from keyexplain import Keyexplain
from staminabar import Staminabar

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
            map.handle_event(event)


def init():
    global map
    global bridge
    global player
    global keyexplain
    global staminabar
    global checktime
    global timelock

    timelock = False
    checktime = get_time()

    map = Map()
    game_world.add_object(map, 0)
    bridge = Bridge()
    game_world.add_object(bridge, 1)
    player = Player()
    game_world.add_object(player, 2)
    keyexplain = Keyexplain()
    game_world.add_object(keyexplain, 3)
    staminabar = Staminabar()
    game_world.add_object(staminabar, 4)

def finish():
    game_world.clear()
    pass

def update():
    global playerx
    global playery
    global playerstamina
    game_world.update()

    playerx = player.x
    playery = player.y
    playerstamina = player.stamina

    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    global pausetime
    global checktime
    global timelock

    player.dirX = 0
    player.dirY = 0
    player.dir_left, player.dir_right, player.dir_up, player.dir_down = 0, 0, 0, 0
    player.dir_lshift = 0
    map.dirX = 0
    map.dirY = 0
    map.dir_left, map.dir_right = 0, 0

    timelock = True
    pausetime = get_time()
    pass

def resume():
    global pausetime
    global resumetime
    global checktime
    global timelock

    timelock = False
    resumetime = get_time()
    checktime += resumetime - pausetime
    pass