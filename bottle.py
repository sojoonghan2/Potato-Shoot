import random

from pico2d import load_image, draw_rectangle, get_time
import play_mode


class Idle:
    @staticmethod
    def do(bottle):
        pass

    @staticmethod
    def enter(bottle, e):
        pass

    @staticmethod
    def exit(bottle, e):
        pass

    @staticmethod
    def draw(bottle):
        bottle.image.clip_composite_draw(0, 0, 500, 654, 0, 'r', bottle.x, bottle.y, 130, 180)


class Fly:
    @staticmethod
    def do(bottle):
        bottle.y += 5

    @staticmethod
    def enter(bottle, e):
        pass

    @staticmethod
    def exit(bottle, e):
        pass

    @staticmethod
    def draw(bottle):
        bottle.image.clip_composite_draw(0, 0, 500, 654, bottle.angle, 'r', bottle.x, bottle.y, 130, 180)


class StateMachine:
    def __init__(self, bottle):
        self.bottle = bottle
        self.cur_state = Idle

    def start(self):
        self.cur_state.enter(self.bottle, ('START', 0))

    def handle_event(self):
        pass

    def update(self):
        self.cur_state.do(self.bottle)

    def draw(self):
        self.cur_state.draw(self.bottle)


class Bottle:
    image = None

    def __init__(self, x=140, y=500):
        if Bottle.image == None:
            Bottle.image = load_image('Resource\\Bottle\\Bottle.png')
        self.x, self.y = x, y
        self.die_time = 0
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.angle = random.randint(1, 6)

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb_r())

    def handle_event(self, event):
        pass

    def update(self):
        self.state_machine.update()

    def get_bb_r(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision_r(self, group, other):
        # 사각형과 사각형 충돌
        if group == 'bottle:potato(r)':
            if play_mode.potato.collision_ok == 1:
                if self.state_machine.cur_state == Idle:
                    if play_mode.potato.player == 0:
                        play_mode.potato.p1_score += 1
                    elif play_mode.potato.player == 1:
                        play_mode.potato.p2_score += 1
                self.state_machine.cur_state = Fly

    def handle_collision_c(self, group, other):
        # 사각형과 원 충돌
        if group == 'bottle:potato(c)':
            # 사각형과 사각형 충돌이 가능하게 됨
            play_mode.potato.collision_ok = 1