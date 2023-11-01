from pico2d import delay, close_canvas, open_canvas
import game_framework
import title_mode

open_canvas(1400, 800)
game_framework.run(title_mode)
close_canvas()