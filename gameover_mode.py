from pico2d import get_events, load_image, clear_canvas, update_canvas, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1

import game_framework
import game_world
import title_mode
from bgm.bgm_sound import Bgm_sound
from level1 import cycler, cycling_mode
from level2 import swimming_mode
from level3 import running_mode


def init():
    global image
    global bgm_sound
    global button_select2
    image = load_image('./resource/gameover.png')
    bgm_sound = Bgm_sound('./bgm/game_over_bgm.mp3')
    button_select2 = load_wav('./bgm/button_select2.wav')
def finish():
    if game_world.level == 1:
        if cycling_mode.cycler.cycler_rock_sound:
            cycling_mode.cycler.cycler_rock_sound = None
        if cycling_mode.cycler.cycler_cliff_sound:
            cycling_mode.cycler.cycler_cliff_sound = None
        if cycling_mode.cycler.cycler_cycle:
            cycling_mode.cycler.cycler_cycle = None
    if game_world.level == 2:
        if swimming_mode.swimmer.swimmer_shark:
            swimming_mode.swimmer.swimmer_shark = None
        if swimming_mode.swimmer.swimmer_swirl:
            swimming_mode.swimmer.swimmer_swirl = None
        if swimming_mode.swimmer.swimmer_swim:
            swimming_mode.swimmer.swimmer_swim = None
    if game_world.level == 3:
        if running_mode.runner.runner_zombie:
            running_mode.runner.runner_zombie = None
        if running_mode.runner.runner_splinter:
            running_mode.runner.runner_splinter = None
        if running_mode.runner.runner_run:
            running_mode.runner.runner_run = None
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
