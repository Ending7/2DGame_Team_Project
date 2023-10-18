from pico2d import load_image


class Map:
    def __init__(self):
        self.image = load_image('map1.png')

    def draw(self):
        self.image.draw(2000 / 1000 + 950 , 800 / 2)

    def update(self):
        pass
