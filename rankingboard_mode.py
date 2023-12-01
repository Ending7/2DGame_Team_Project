from pico2d import get_events, load_image, clear_canvas, update_canvas, load_font, load_wav
from sdl2 import SDL_QUIT, SDL_KEYDOWN, SDLK_ESCAPE, SDLK_1

import game_framework
import game_world
import title_mode
from bgm.bgm_sound import Bgm_sound


def init():
    global image
    global font
    global bgm_sound
    global button_select2
    image = load_image('./resource/rankingboard.png')
    font = load_font('./resource/ENCR10B.TTF', 15)
    bgm_sound = Bgm_sound('./bgm/ranking_bgm.mp3')
    button_select2 = load_wav('./bgm/button_select2.wav')

def finish():
    bgm_sound.bgm.stop()
    pass


def update():
    pass


def draw():
    clear_canvas()
    image.draw(1400 / 2, 800 / 2)
    if game_world.record_sum[0]:
        font.draw(230, 635, f'(cycling:{game_world.record_sum[0][0]}, swimming:{game_world.record_sum[0][1]}, running:{game_world.record_sum[0][2]}, sum:{game_world.record_sum[0][3]})', (255, 0, 0))
    if game_world.record_sum[1]:
        font.draw(230, 540, f'(cycling:{game_world.record_sum[1][0]}, swimming:{game_world.record_sum[1][1]}, running:{game_world.record_sum[1][2]}, sum:{game_world.record_sum[1][3]})', (255, 0, 0))
    if game_world.record_sum[2]:
        font.draw(230, 445, f'(cycling:{game_world.record_sum[2][0]}, swimming:{game_world.record_sum[2][1]}, running:{game_world.record_sum[2][2]}, sum:{game_world.record_sum[2][3]})', (255, 0, 0))
    if game_world.record_sum[3]:
        font.draw(230, 350, f'(cycling:{game_world.record_sum[3][0]}, swimming:{game_world.record_sum[3][1]}, running:{game_world.record_sum[3][2]}, sum:{game_world.record_sum[3][3]})', (255, 0, 0))
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
