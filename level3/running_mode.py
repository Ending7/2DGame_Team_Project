from pico2d import *
import random
import game_world
import game_framework
import gameclear_mode
import gameover_mode
import pause_mode
import title_mode
from level3.splinter import Splinter
from level3.runner import Runner
from key_explain import Keyexplain
from level3.runner_stamina import Runner_stamina
from level3.running_map import Running_map


def runner_idle():
    runner.dirX = 0
    runner.dirY = 0
    runner.dir_left, runner.dir_right, runner.dir_up, runner.dir_down = 0, 0, 0, 0
    runner.dir_lshift = 0
    running_map.dirX = 0
    running_map.dirY = 0
    running_map.dir_left, running_map.dir_right = 0, 0
    runner.state_machine.handle_event(('LETS_IDLE', 0))


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

    splinters = [Splinter(random.randint(400, 400), random.randint(0, 400), random.randint(1, 2), 0) for _ in range(50)]
    splinters += [Splinter(random.randint(200, 200), random.randint(0, 400), random.randint(1, 2), 3) for _ in range(50)]
    splinters += [Splinter(random.randint(600, 900), random.randint(0, 400), random.randint(1, 2), random.randint(0, 6)) for _ in range(30)]
    splinters += [Splinter(random.randint(900, 1200), random.randint(0, 400), random.randint(1, 2), random.randint(0, 6)) for _ in range(30)]
    game_world.add_objects(splinters, 1)
    for splinter in splinters:
        game_world.add_collision_pair('runner:splinter', None, splinter)

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
            game_framework.change_mode(title_mode)
        elif event.type == SDL_KEYDOWN and event.key == SDLK_p:
            game_framework.push_mode(pause_mode)
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

    time_lock = False
    check_time = get_time()
    # 객체 생성
    create_object()

    # 충돌 상황 등록


def finish():
    game_world.remove_all_object('runner:splinter')
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
