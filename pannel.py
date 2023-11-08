from pico2d import load_image

class Pannel:
    def __init__(self):
        self.image = load_image('./resource/pause.png')

    def draw(self):
        self.image.draw(1400/2, 800/2)

    def update(self):
        pass