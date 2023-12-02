from pico2d import *
import random
import game_world
import game_framework
import gameclear_mode
import gameover_mode
import pause_mode
import title_mode
from bgm.bgm_sound import Bgm_sound
from level3.splinter import Splinter
from level3.runner import Runner
from key_explain import Keyexplain
from level3.runner_stamina import Runner_stamina
from level3.running_map import Running_map
from level3.zombie import Zombie


def runner_idle():
    runner.dirX = 0
    runner.dirY = 0
    runner.dir_left, runner.dir_right, runner.dir_up, runner.dir_down = 0, 0, 0, 0
    runner.dir_lshift = 0
    running_map.dirX = 0
    running_map.dirY = 0
    running_map.dir_left, running_map.dir_right = 0, 0
    runner.state_machine.handle_event(('LETS_IDLE', 0))


def create_outside_splinter():
    splinters = []
    start = 130
    for _ in range(8):
        splinters.append(Splinter(start, 410, 1, 0))
        start += 200
    start = 130
    for _ in range(8):
        splinters.append(Splinter(start, 30, 1, 0))
        start += 200

    game_world.add_objects(splinters, 1)
    for splinter in splinters:
        game_world.add_collision_pair('runner:splinter', None, splinter)


def create_inside_splinter():
    splinters = []
    start = 130

    for _ in range(8):
        splinters.append(Splinter(start, 360, 2, 5))
        start += 50
    start = 130
    for _ in range(8):
        splinters.append(Splinter(start, 50, 2, 4))
        start += 50
    start = 85
    for _ in range(9):
        splinters.append(Splinter(130, start, 2, 3))
        start += 30
    start = 85
    for _ in range(9):
        splinters.append(Splinter(250, start, 2, 2))
        start += 30
    start = 85
    for _ in range(9):
        splinters.append(Splinter(370, start, 2, 1))
        start += 30
    start = 85
    for _ in range(9):
        splinters.append(Splinter(480, start, 2, 0))
        start += 30

    game_world.add_objects(splinters, 1)
    for splinter in splinters:
        game_world.add_collision_pair('runner:splinter', None, splinter)


def create_inside2_splinter():
    splinters = []
    start = 10
    for _ in range(14):
        splinters.append(Splinter(635, start, 2, random.randint(0, 6)))
        start += 30
    start = 10
    for _ in range(14):
        splinters.append(Splinter(835, start, 2, random.randint(0, 6)))
        start += 30
    start = 10
    for _ in range(14):
        splinters.append(Splinter(1035, start, 2, random.randint(0, 6)))
        start += 30
    start = 10
    for _ in range(14):
        splinters.append(Splinter(1235, start, 2, random.randint(0, 6)))
        start += 30
    game_world.add_objects(splinters, 1)
    for splinter in splinters:
        game_world.add_collision_pair('runner:splinter', None, splinter)


def create_object():
    global running_map
    global runner
    global splinters
    global keyexplain
    global runner_stamina

    running_map = Running_map()
    game_world.add_object(running_map, 0)

    runner = Runner()
    game_world.add_object(runner, 2)
    game_world.add_collision_pair('runner:splinter', runner, None)
    game_world.add_collision_pair('runner:zombie', runner, None)

    key_explain = Keyexplain()
    game_world.add_object(key_explain, 3)
    runner_stamina = Runner_stamina()
    game_world.add_object(runner_stamina, 4)


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            runner.runner_run = None
            button_select2.play()
            game_world.delete_record_time()
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            runner.runner_run = None
            button_select1.play()
            game_framework.push_mode(pause_mode)
            runner.runner_run = load_wav('./bgm/runner_run.wav')
        elif event.type == SDL_KEYDOWN and event.key == SDLK_1:
            if game_world.item[0] == 1:
                runner.runner_run = None
                use_stamina_item.play()
                runner.stamina = 65
                game_world.item[0] = 0
                runner.runner_run = load_wav('./bgm/runner_run.wav')
        elif event.type == SDL_KEYDOWN and event.key == SDLK_2:
            if game_world.item[1] == 1:
                if runner.invisibility_mode == False:
                    runner.speed_mode = True
                    runner.runner_run = None
                    use_speed_item.play()
                    game_world.item[1] = 0
                    runner.runner_run = load_wav('./bgm/runner_run.wav')
        elif event.type == SDL_KEYDOWN and event.key == SDLK_3:
            if game_world.item[2] == 1:
                if runner.speed_mode == False:
                    runner.runner_run = None
                    runner.invisibility_mode = True
                    use_invisibility_item.play()
                    game_world.item[2] = 0
                    runner.runner_run = load_wav('./bgm/runner_run.wav')
        else:
            runner.handle_event(event)


def init():
    global running_map
    global bridge
    global runner
    global keyexplain
    global runner_stamina
    global check_time
    global time_lock
    global item_image1
    global item_image2
    global item_image3
    global item_no_image
    global bgm_sound
    global use_stamina_item
    global use_speed_item
    global use_invisibility_item
    global button_select1
    global button_select2
    game_world.level = 3
    item_image1 = load_image('./resource/stamina.png')
    item_image2 = load_image('./resource/speedup.png')
    item_image3 = load_image('./resource/invisibility.png')
    item_no_image = load_image('./resource/noitem.png')

    time_lock = False
    check_time = get_time()
    # 객체 생성
    create_object()
    create_outside_splinter()
    create_inside_splinter()
    create_inside2_splinter()

    zombie = Zombie(1300, 230)
    game_world.add_object(zombie, 2)
    game_world.add_collision_pair('runner:zombie', None, zombie)

    bgm_sound = Bgm_sound('./bgm/level3_bgm.mp3')
    use_stamina_item = load_wav('./bgm/use_stamina_item.wav')
    use_speed_item = load_wav('./bgm/use_speed_item.wav')
    use_invisibility_item = load_wav('./bgm/use_invisibility_item.wav')
    button_select1 = load_wav('./bgm/button_select.wav')
    button_select2 = load_wav('./bgm/button_select2.wav')
def finish():
    bgm_sound.bgm.stop()
    game_world.remove_all_object('runner:splinter')
    game_world.remove_all_object('runner:zombie')
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collision()
    if runner.die:
        game_framework.change_mode(gameover_mode)
    if runner.success:
        game_framework.change_mode(gameclear_mode)

def draw():
    clear_canvas()
    game_world.render()
    if game_world.item[0] == 1:
        item_image1.draw(2000 / 1000 + 50, 800 / 2 + 250)
    else:
        item_no_image.draw(2000 / 1000 + 50, 800 / 2 + 250)
    if game_world.item[1] == 1:
        item_image2.draw(2000 / 1000 + 170, 800 / 2 + 250)
    else:
        item_no_image.draw(2000 / 1000 + 170, 800 / 2 + 250)

    if game_world.item[2] == 1:
        item_image3.draw(2000 / 1000 + 290, 800 / 2 + 250)
    else:
        item_no_image.draw(2000 / 1000 + 290, 800 / 2 + 250)
    update_canvas()
def pause():
    global pause_time
    global check_time
    global time_lock
    time_lock = True
    pause_time = get_time()
    runner_idle()
    pass


def resume():
    global pause_time
    global resume_time
    global check_time
    global time_lock

    time_lock = False
    resume_time = get_time()
    check_time += resume_time - pause_time
    pass
