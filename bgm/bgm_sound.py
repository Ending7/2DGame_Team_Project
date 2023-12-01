from pico2d import load_image, load_music, load_wav


class Bgm_sound:
    def __init__(self, music_name):
        self.bgm = load_music(music_name)
        self.bgm.set_volume(32)
        self.bgm.repeat_play()


def draw(self):
    pass

def update(self):
    pass

def finish(self):
    pass
