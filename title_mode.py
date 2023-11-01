from pico2d import get_events, load_image, clear_canvas, update_canvas, get_time
import game_framework

def init():
    global image
    global title_start_time
    title_start_time = get_time()
    image = load_image('title.png')

def finish():
    pass

def update():
    if get_time() - title_start_time >= 2.0:
        game_framework.quit()
    pass

def draw():
    clear_canvas()
    image.draw(1400 / 2, 800 / 2)
    update_canvas()

def handle_events():
    events = get_events()