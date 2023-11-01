from pico2d import *

import game_world
from player import Player
from map import Map
from bridge import Bridge


# Game object class here
def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)
            map.handle_event(event)


def init():
    global running
    global player
    global map
    global bridge
    running = True
    map = Map()
    game_world.add_object(map, 0)
    bridge = Bridge()
    game_world.add_object(bridge, 1)
    player = Player()
    game_world.add_object(player, 2)


def finish():
    pass


def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()
