from pico2d import load_image

class Keyexplain:
    def __init__(self):
        self.image = load_image('keyexplain.png')

    def draw(self):
        self.image.draw(70, 760)

    def update(self):
        pass