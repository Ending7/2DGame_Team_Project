from pico2d import load_image


class Bridge:
    def __init__(self):
        self.image = load_image('bridge.png')

    def draw(self):
        self.image.draw(1400 / 2, 800 / 2, 1440, 350)

    def update(self):
        pass
