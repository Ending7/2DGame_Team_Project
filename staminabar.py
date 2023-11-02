from pico2d import load_image
import play_mode

class Staminabar:
    def __init__(self):
        self.image = load_image('staminabar.png')

    def draw(self):
        self.image.draw(play_mode.playerx- 30 + play_mode.playerstamina / 2
                        , play_mode.playery + 40, 0 + play_mode.playerstamina, 10)

    def update(self):
        pass