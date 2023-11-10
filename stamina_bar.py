from pico2d import load_image
import cycling_mode


class Staminabar:
    def __init__(self):
        self.image = load_image('./resource/staminabar.png')

    def draw(self):
        self.image.draw(cycling_mode.player.x - 30 + cycling_mode.player.stamina / 2
                        , cycling_mode.player.y + 40, 0 + cycling_mode.player.stamina, 10)

    def update(self):
        pass
