from pico2d import load_image, load_wav


class Swimming_map:
    def __init__(self):
        self.image = load_image('./resource/swimmingmap.png')
        self.x = 0

    def draw(self):
        self.image.draw(1400/2,800/2)

    def update(self):
        pass

