from pico2d import *
import game_framework
import game_world
from ground import Ground
from potato import Potato
from bottle import Bottle
from water import Water
from sdl2 import SDL_KEYDOWN
import title_mode


def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.change_mode(title_mode)
        else:
            potato.handle_event(event)


def init():
    global running
    global ground
    global team
    global world
    global potato
    global bottle
    global water
    world = []

    # 땅
    ground = Ground()
    game_world.add_object(ground, 0)

    # 물
    water_positions = [
        # 왼
        (-230, -120),
        # 오
        (230, -120)
    ]

    for position in water_positions:
        water = Water(*position)
        game_world.add_object(water, 1)

    # 병
    bottle_positions = [
        # 4열
        (150, 900), (230, 900), (310, 900), (390, 900),
        # 3열
        (190, 870), (270, 870), (350, 870),
        # 2열
        (230, 840), (310, 840),
        # 1열
        (270, 810)
    ]

    bottle = [Bottle(*bottle_positions[i]) for i in range(10)]
    game_world.add_objects(bottle, 2)

    # 감자
    potato = Potato(270, 100)
    game_world.add_object(potato, 2)
    game_world.add_collision_pair('bottle:potato(r)', None, potato)
    game_world.add_collision_pair('bottle:potato(c)', None, potato)

    for i in range(10):
        game_world.add_collision_pair('bottle:potato(r)', bottle[i], None)
        game_world.add_collision_pair('bottle:potato(c)', bottle[i], None)

    print('--------')
    print('Frame 1')


def finish():
    game_world.clear()
    pass


def update():
    game_world.update()
    game_world.handle_collisions()


def draw():
    clear_canvas()
    game_world.render()
    update_canvas()


def pause():
    pass


def resume():
    pass


def next_stage():
    bottle_positions = [
        # 4열
        (150, 900), (230, 900), (310, 900), (390, 900),
        # 3열
        (190, 870), (270, 870), (350, 870),
        # 2열
        (230, 840), (310, 840),
        # 1열
        (270, 810)
    ]
    for i in range(10):
        game_world.remove_object(bottle[i])
    bottle2 = [Bottle(*bottle_positions[i]) for i in range(10)]
    # bottle을 지우고 bottle을 다시 만들면 오류가 나지만
    # bottle을 지우고 bottle2를 만들고 bottle2를 bottle에 넣으면 오류가 안남 왜지??
    for i in range(10):
        bottle[i] = bottle2[i]
        game_world.add_collision_pair('bottle:potato(r)', bottle[i], None)
        game_world.add_collision_pair('bottle:potato(c)', bottle[i], None)
    game_world.add_objects(bottle, 2)