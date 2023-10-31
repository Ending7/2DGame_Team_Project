from pico2d import delay, close_canvas, open_canvas

import play_mode
open_canvas(1400, 800)
play_mode.init()
# game loop
while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.draw()
    delay(0.01)
# finalization code
close_canvas()