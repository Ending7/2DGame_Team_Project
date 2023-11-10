from pico2d import load_image
import game_framework
import play_mode

PIXEL_PER_METER = (10.0 / 0.3)  # m당 몇 픽셀이냐 / 10px에 30cm. 10px에 0.3m.
RUN_SPEED_KMPH = 10.0  # Km / Hour 한 시간에 마라톤 선수가 대략 20km를 달린다.
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)  # 1분에 몇m 움직였는지
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)  # 1초에 몇m 움직였는지 알아야 한다.
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)  # 초당 몇 픽셀만큼 움직이는지. 미터당 비례하는 픽셀 수를 알았으니, 1초에 움직인 m * 픽셀수를 곱해주면 나온다.


class Cycling_map:
    def __init__(self):
        self.image = load_image('./resource/cyclingmap.png')
        self.x = 0

    def draw(self):
        self.image.draw(2000 / 1000 + 950 + self.x, 800 / 2)

    def update(self):
        if play_mode.player.stamina_lock == False:
            self.x -= play_mode.player.dirX * RUN_SPEED_PPS * game_framework.frame_time * play_mode.player.speed
        if self.x <= -500:
            self.x = -500
        elif self.x >= 45:
            self.x = 45
