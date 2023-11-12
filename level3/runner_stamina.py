from pico2d import load_image
from level3 import running_mode


class Runner_stamina:
    def __init__(self):
        self.image = load_image('./resource/staminabar.png')

    def draw(self):
        self.image.draw(running_mode.runner.x - 25 + running_mode.runner.stamina / 2
                        , running_mode.runner.y + 50, 0 + running_mode.runner.stamina, 10)

    def update(self):
        pass
