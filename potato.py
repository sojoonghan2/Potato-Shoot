from pico2d import load_image, draw_rectangle
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_a

import game_framework
import play_mode
from point import Point


def right_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def space_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


def a_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


# 대기
class Idle:
    @staticmethod
    def do(potato):
        pass

    @staticmethod
    def enter(potato, e):
        pass

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)


# 좌우 이동
class Moving:
    @staticmethod
    def do(potato):
        if potato.x > 400 and potato.dir == 1:
            return
        if potato.x < 140 and potato.dir == -1:
            return
        potato.x += potato.dir * 1

    @staticmethod
    def enter(potato, e):
        if right_down(e) or left_up(e):
            potato.dir = 1
        elif left_down(e) or right_up(e):
            potato.dir = -1

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)


# 굴리기 전 파워 설정
class PowerCharging:
    @staticmethod
    def do(potato):
        # 디버깅 코드
        # 파워를 강제로 변환
        # 높은 파워
        # potato.power = 90
        # 낮은 파워
        # potato.power = 10
        # 직접 조작
        potato.power += 1
        if potato.power > 100:
            potato.power = 0

    @staticmethod
    def enter(potato, e):
        pass

    @staticmethod
    def exit(potato, e):
        potato.speed -= potato.power / 100
        potato.bb += potato.power

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        for i in range(0, potato.power):
            draw_rectangle(100, 300, 100 + i * 3.5, 400)
        draw_rectangle(100, 300, 450, 400)


# 굴리기 전 각도 설정
class AngleAdjustment:
    @staticmethod
    def do(potato):
        if potato.way == 0:
            point.dir = 1
        elif potato.way == 1:
            point.dir = -1
        if potato.angle > 1.5:
            potato.way = 1
        elif potato.angle < -1.5:
            potato.way = 0
        potato.angle += point.dir * 0.02

    @staticmethod
    def enter(potato, e):
        # 화살표
        global point
        point = Point(potato.x - 50, potato.y + 30)

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        point.image.clip_composite_draw(0, 0, 150, 150, potato.angle, 'r', potato.x, potato.y + 120, 100, 100)


# 굴리기
class Rolling:
    @staticmethod
    def do(potato):
        # 굴러감
        potato.y += potato.speed
        # 굴러가면서 크기 작아짐
        if potato.size > 10:
            potato.size -= potato.speed / 10
        # 감자의 각도에 따라 굴러가는 각도 변경
        potato.x -= potato.angle
        # 감자의 힘에 따라서 굴러가는 스핀 변경
        potato.spin += potato.power / 500
        # 일정 범위 넘으면 감자 속성 초기화
        if potato.y > 1500:
            # 위치
            potato.x = 270
            potato.y = 100
            # 크기
            potato.size = 150
            # 스핀
            potato.spin = 0
            # 힘
            potato.power = 0
            # 속도
            potato.speed = 5
            # 충돌범위
            potato.bb = 0
            # 각도
            potato.angle = 0
            # dir
            potato.dir = 1
            # 현재 플레이어의 턴을 -1
            potato.turn -= 1
            # 충돌 ok
            potato.collision_ok = 0
            # 현재 상태
            potato.state_machine.cur_state = Idle
            # 턴이 종료되면
            if potato.turn == 0 or potato.p1_score == 10 or potato.p2_score == 10:
                # 플레이어 변경
                if potato.player == 0:
                    potato.p1_score = 0
                    potato.player = 1
                else:
                    potato.p2_score = 0
                    potato.player = 0
                    # 게임의 턴을 증가
                    potato.t_turn += 1
                    print('Frame', potato.t_turn + 1)
                    # 게임이 종료되면
                    if potato.t_turn == 10:
                        # 프레임워크 변경(play_mode가 아닌 ending_mode로 넘어가도록 수정)
                        game_framework.change_mode(play_mode)
                # 턴 개수 회복(10번째 턴은 3번 굴림)
                if potato.t_turn == 9:
                    potato.turn = 3
                else:
                    potato.turn = 2
                # next_state 활성화
                play_mode.next_stage()

    @staticmethod
    def enter(potato, e):
        pass

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, potato.spin, 'r', potato.x, potato.y + 20, potato.size,
                                             potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, potato.spin, 'r', potato.x, potato.y + 20, potato.size,
                                              potato.size)


class Giant:
    @staticmethod
    def do(potato):
        if potato.size < 200:
            potato.size += 0.1
        else:
            potato.state_machine.cur_state = Idle

    @staticmethod
    def enter(potato, e):
        # 능력 발동을 한 상태가 아니면(중복 방지)
        if potato.size < 200:
            if potato.player == 0:
                # 능력 개수가 0이 아니면
                if potato.p1_ability > 0:
                    # 능력 개수를 1 깎음
                    potato.p1_ability -= 1
                    # bb 범위 증가
                    potato.bb += 50
                else:
                    potato.state_machine.cur_state = Idle
            elif potato.player == 1:
                # 능력 개수가 0이 아니면
                if potato.p2_ability > 0:
                    # 능력 개수를 1 깎음
                    potato.p2_ability -= 1
                    # bb 범위 증가
                    potato.bb += 50
                else:
                    potato.state_machine.cur_state = Idle

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)


class StateMachine:
    def __init__(self, potato):
        self.potato = potato
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Moving, left_down: Moving, left_up: Moving, right_up: Moving, space_down: PowerCharging,
                   a_down: Giant},
            Moving: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle},
            PowerCharging: {space_down: AngleAdjustment},
            AngleAdjustment: {space_down: Rolling},
            Giant: {},
            Rolling: {}
        }

    def start(self):
        self.cur_state.enter(self.potato, ('START', 0))

    def handle_event(self, e):
        for check_event, next_state in self.table[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.potato, e)
                self.cur_state = next_state
                self.cur_state.enter(self.potato, e)
                return True
        return False

    def update(self):
        self.cur_state.do(self.potato)

    def draw(self):
        self.cur_state.draw(self.potato)


class Potato:
    def __init__(self, x=300, y=90):
        self.player = 0
        self.collision_ok = 0
        self.x, self.y = x, y
        self.spin = 0
        self.power = 0
        self.angle = 0
        self.dir = 1
        self.way = 0
        self.turn = 2
        self.size = 150
        self.speed = 5
        self.bb = 0
        self.p1_ability = 2
        self.p2_ability = 2
        self.p1_score = 0
        self.p2_score = 0
        self.p1_t_score = 0
        self.p2_t_score = 0
        self.t_turn = 0
        self.image = load_image('Resource\\Potato\\normal1.png')
        self.image2 = load_image('Resource\\Potato\\giant1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        draw_rectangle(*self.get_bb_r())
        draw_rectangle(*self.get_bb_c_1())
        draw_rectangle(*self.get_bb_c_2())
        draw_rectangle(*self.get_bb_c_3())
        draw_rectangle(*self.get_bb_c_4())
        draw_rectangle(*self.get_bb_c_5())
        draw_rectangle(*self.get_bb_c_6())

    def get_bb_r(self):
        return self.x - self.bb - 10, self.y - self.bb, self.x + self.bb + 10, self.y + self.bb + 20

    def get_bb_c_1(self):
        return self.x - 12, self.y + 2, self.x + 12, self.y + 54

    def get_bb_c_2(self):
        return self.x - 15, self.y + 5, self.x + 15, self.y + 51

    def get_bb_c_3(self):
        return self.x - 18, self.y + 8, self.x + 18, self.y + 48

    def get_bb_c_4(self):
        return self.x - 21, self.y + 11, self.x + 21, self.y + 45

    def get_bb_c_5(self):
        return self.x - 24, self.y + 13, self.x + 24, self.y + 42

    def get_bb_c_6(self):
        return self.x - 27, self.y + 17, self.x + 27, self.y + 39

    def handle_collision_r(self, group, other):
        # 사각형과 사각형 충돌
        if group == 'bottle:potato(r)':
            pass

    def handle_collision_c(self, group, other):
        # 사각형과 원 충돌
        if group == 'bottle:potato(c)':
            pass
