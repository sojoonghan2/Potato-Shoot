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
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def update(self):
        self.state_machine.update()

    def get_bb(self):
        return self.x - 20, self.y - 50, self.x + 20, self.y + 50

    def handle_collision(self, group, other):
        if group == 'potato:bottle':
            if self.state_machine.cur_state == Idle:
                # potato.crash += 1
                pass
            self.state_machine.cur_state = Fly

