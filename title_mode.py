from pico2d import get_events, load_image, clear_canvas, update_canvas
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1, SDLK_2, SDLK_3

import game_framework
import game_world
import howtoplay_mode
from level1 import cycling_mode
import rankingboard_mode
import pickle
def init():
    global image
    with open("data.p", 'rb') as f:
        game_world.record_sum = pickle.load(f)
    image = load_image('./resource/title.png')


def finish():
    pass


def update():
    game_world.delete_record_time()
    pass


def draw():
    clear_canvas()
    image.draw(1400 / 2, 800 / 2)
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.quit()
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_1):
            game_framework.change_mode(cycling_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            game_framework.change_mode(howtoplay_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            game_framework.change_mode(rankingboard_mode)


def pause():
    pass


def resume():
    pass
