from pico2d import *
import game_world
import game_framework
import title_mode
from pannel import Pannel


# Game object class here
def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            button_select2 .play()
            game_framework.pop_mode()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_s:
            button_select2.play()
            game_framework.pop_mode()


def init():
    global pannel
    global button_select2
    pannel = Pannel()
    game_world.add_object(pannel, 5)
    button_select2 = load_wav('./bgm/button_select2.wav')

def update():
    game_world.update()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def finish():
    game_world.remove_object(pannel)
    pass


def pause():
    pass


def resume():
    pass
