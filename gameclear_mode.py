from pico2d import get_events, load_image, clear_canvas, update_canvas, load_font, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1

import game_framework
import game_world
import title_mode
import pickle

from bgm.bgm_sound import Bgm_sound


def init():
    global image
    global font
    global bgm_sound
    global button_select2
    font = load_font('./resource/ENCR10B.TTF', 20)
    image = load_image('./resource/gameclear.png')
    bgm_sound = Bgm_sound('./bgm/game_clear_bgm.mp3')
    button_select2 = load_wav('./bgm/button_select2.wav')
def finish():
    bgm_sound.bgm.stop()
    with open('data.p', 'wb') as f:
        pickle.dump(game_world.record_sum, f)
    game_world.delete_record_time()
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(1400 / 2, 800 / 2)
    font.draw(30, 750, f'(cycling:{game_world.records[0]}, swimming:{game_world.records[1]}, running:{game_world.records[2]}, sum:{game_world.records[3]})', (255, 0, 0))
    update_canvas()


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            button_select2.play()
            game_world.delete_record_time()
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
