from pico2d import load_image
from level2 import swimming_mode


class Swimmer_stamina:
    def __init__(self):
        self.image = load_image('./resource/staminabar.png')

    def draw(self):
        self.image.draw(swimming_mode.swimmer.x - 25 + swimming_mode.swimmer.stamina / 2
                        , swimming_mode.swimmer.y + 30, 0 + swimming_mode.swimmer.stamina, 10)

    def update(self):
        pass
