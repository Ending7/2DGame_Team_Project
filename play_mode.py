from pico2d import *
import game_world
import game_framework
import pause_mode
import title_mode
from player import Player
from map import Map
from bridge import Bridge
from keyexplain import Keyexplain

# Game object class here
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

    map = Map()
    game_world.add_object(map, 0)
    bridge = Bridge()
    game_world.add_object(bridge, 1)
    player = Player()
    game_world.add_object(player, 2)
    keyexplain = Keyexplain()
    game_world.add_object(keyexplain, 3)

def finish():
    game_world.clear()
    pass

def update():
    game_world.update()
    delay(0.01)

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def pause():
    player.dirX = 0
    player.dirY = 0
    player.dir_left, player.dir_right, player.dir_up, player.dir_down = 0, 0, 0, 0
    map.dirX = 0
    map.dirY = 0
    map.dir_left, map.dir_right = 0, 0

def resume():
    pass