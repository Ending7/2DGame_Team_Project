from pico2d import load_image
from level1 import cycling_mode


class Cycler_stamina:
    def __init__(self):
        self.image = load_image('./resource/staminabar.png')

    def draw(self):
        self.image.draw(cycling_mode.cycler.x - 30 + cycling_mode.cycler.stamina / 2
                        , cycling_mode.cycler.y + 40, 0 + cycling_mode.cycler.stamina, 10)

    def update(self):
        pass
