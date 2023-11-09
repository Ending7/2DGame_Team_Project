from pico2d import load_image
import play_mode


class Staminabar:
    def __init__(self):
        self.image = load_image('./resource/staminabar.png')

    def draw(self):
        self.image.draw(play_mode.player.x - 30 + play_mode.player.stamina / 2
                        , play_mode.player.y + 40, 0 + play_mode.player.stamina, 10)

    def update(self):
        pass
