from pico2d import get_events, load_image, clear_canvas, update_canvas, load_music, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1, SDLK_2, SDLK_3

import game_framework
import game_world
import howtoplay_mode
from bgm.bgm_sound import Bgm_sound
from level1 import cycling_mode
from level2 import swimming_mode
from level3 import running_mode
import rankingboard_mode
import pickle
def init():
    global image
    global bgm_sound
    with open("data.p", 'rb') as f:
        game_world.record_sum = pickle.load(f)
    image = load_image('./resource/title.png')

    bgm_sound = Bgm_sound('./bgm/title_bgm.mp3')

def finish():
    game_world.clear()
    bgm_sound.bgm.stop()
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
            game_world.item[0] = 1
            game_world.item[1] = 1
            game_world.item[2] = 1
            game_framework.change_mode(cycling_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_2):
            game_framework.change_mode(howtoplay_mode)
        elif (event.type, event.key) == (SDL_KEYDOWN, SDLK_3):
            game_framework.change_mode(rankingboard_mode)


def pause():
    pass


def resume():
    pass
