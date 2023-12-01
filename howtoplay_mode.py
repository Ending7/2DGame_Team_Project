from pico2d import get_events, load_image, clear_canvas, update_canvas, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1

import game_framework
import title_mode
from bgm.bgm_sound import Bgm_sound


def init():
    global image
    global bgm_sound
    global button_select2
    image = load_image('./resource/howtoplay.png')
    bgm_sound = Bgm_sound('./bgm/how_to_bgm.mp3')
    button_select2 = load_wav('./bgm/button_select2.wav')
def finish():
    bgm_sound.bgm.stop()
    pass


def update():
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
            button_select2.play()
            game_framework.change_mode(title_mode)


def pause():
    pass


def resume():
    pass
