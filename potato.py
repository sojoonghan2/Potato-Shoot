from pico2d import load_image, draw_rectangle, load_font, load_wav
from sdl2 import SDL_KEYDOWN, SDLK_RIGHT, SDL_KEYUP, SDLK_LEFT, SDLK_SPACE, SDLK_a, SDLK_b

import game_framework
import play_mode
from point import Point
from board import Board
import ending_mode1, ending_mode2, ending_mode3


def right_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def space_up(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_SPACE


def a_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def b_down(e): return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_b


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
        potato.x += potato.dir

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
        potato.powerchargingBGM.play()

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
            potato.reset_potato()

    @staticmethod
    def enter(potato, e):
        potato.rollingBGM.play()

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
                    # 효과음 재생
                    potato.giantBGM.play()
                    # 능력 개수를 1 깎음
                    potato.p1_ability -= 1
                    # 능력이 발동
                    potato.giant = 1
                    # bb 범위 증가
                    potato.bb += 50
                else:
                    potato.state_machine.cur_state = Idle
            elif potato.player == 1:
                # 능력 개수가 0이 아니면
                if potato.p2_ability > 0:
                    # 효과음 재생
                    potato.giantBGM.play()
                    # 능력 개수를 1 깎음
                    potato.p2_ability -= 1
                    # 능력이 발동
                    potato.giant = 1
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


class ScoreCheck:
    @staticmethod
    def do(potato):
        pass

    @staticmethod
    def enter(potato, e):
        potato.scorecheckBGM.play()
        global board1
        global board2
        board1 = Board(0, 0)
        board2 = Board(0, 0)

    @staticmethod
    def exit(potato, e):
        pass

    @staticmethod
    def draw(potato):
        if potato.player == 0:
            potato.image.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        elif potato.player == 1:
            potato.image2.clip_composite_draw(0, 0, 150, 150, 0, 'r', potato.x, potato.y + 20, potato.size, potato.size)
        # 보드판 출력
        board1.image.clip_composite_draw(0, 0, 700, 100, 0, 'r', 250, 600, 500, 100)
        board2.image.clip_composite_draw(0, 0, 700, 100, 0, 'r', 250, 500, 500, 100)
        # P1, P2 출력
        potato.font.draw(40, 590, 'P1', (0, 0, 0))
        potato.font.draw(40, 490, 'P2', (0, 0, 0))
        # 총점 출력
        potato.font.draw(450, 590, f'{potato.p1_t_score:d}', (0, 0, 0))
        potato.font.draw(450, 490, f'{potato.p2_t_score:d}', (0, 0, 0))
        # 중간 점수 출력
        for i in range(potato.t_turn):
            if potato.p1_ss[i] == 2:
                potato.font.draw(80 + (i * 35), 600, 'X', (0, 0, 0))
            else:
                potato.font.draw(80 + (i * 35), 600, f'{potato.p1_save_f1_score[i]:d}', (0, 0, 0))
            if potato.p1_ss[i] == 1:
                potato.font.draw(100 + (i * 35), 600, '/', (0, 0, 0))
            elif potato.p1_ss[i] == 0:
                potato.font.draw(100 + (i * 35), 600, f'{potato.p1_save_f2_score[i]:d}', (0, 0, 0))
            potato.font.draw(80 + (i * 35), 570, f'{potato.p1_save_f_score[i]:d}', (0, 0, 0))
        for i in range(potato.t_turn):
            if potato.p2_ss[i] == 2:
                potato.font.draw(80 + (i * 35), 500, 'X', (0, 0, 0))
            else:
                potato.font.draw(80 + (i * 35), 500, f'{potato.p2_save_f1_score[i]:d}', (0, 0, 0))
            if potato.p2_ss[i] == 1:
                potato.font.draw(100 + (i * 35), 500, '/', (0, 0, 0))
            elif potato.p2_ss[i] == 0:
                potato.font.draw(100 + (i * 35), 500, f'{potato.p2_save_f2_score[i]:d}', (0, 0, 0))
            potato.font.draw(80 + (i * 35), 470, f'{potato.p2_save_f_score[i]:d}', (0, 0, 0))


class StateMachine:
    def __init__(self, potato):
        self.potato = potato
        self.cur_state = Idle
        self.table = {
            Idle: {right_down: Moving, left_down: Moving, left_up: Moving, right_up: Moving, space_down: PowerCharging,
                   a_down: Giant, b_down: ScoreCheck},
            ScoreCheck: {b_down: Idle, space_down: Idle},
            Moving: {right_down: Idle, left_down: Idle, left_up: Idle, right_up: Idle, space_down: PowerCharging},
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
        self.giant = 0
        self.p1_ability = 2
        self.p2_ability = 2
        self.p1_f1_score = 0
        self.p1_f2_score = 0
        self.p2_f1_score = 0
        self.p2_f2_score = 0
        self.p1_t_score = 0
        self.p2_t_score = 0
        self.t_turn = 0
        self.p1_save_f_score = []
        self.p2_save_f_score = []
        self.p1_save_f1_score = []
        self.p2_save_f1_score = []
        self.p1_save_f2_score = []
        self.p2_save_f2_score = []
        self.p1_ss = []
        self.p2_ss = []
        self.image = load_image('Resource\\Potato\\normal1.png')
        self.image2 = load_image('Resource\\Potato\\giant1.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()
        self.font = load_font('ENCR10B.TTF', 16)
        self.rollingBGM = load_wav('Resource\\BGM\\rollingBGM.mp3')
        self.rollingBGM.set_volume(15)
        self.giantBGM = load_wav('Resource\\BGM\\giantBGM.mp3')
        self.giantBGM.set_volume(20)
        self.powerchargingBGM = load_wav('Resource\\BGM\\powerchargingBGM.mp3')
        self.powerchargingBGM.set_volume(15)
        self.scorecheckBGM = load_wav('Resource\\BGM\\scorecheckBGM.mp3')
        self.scorecheckBGM.set_volume(15)

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
        if self.t_turn == 10:
            self.font.draw(330, 750, '!last frame!', (0, 0, 0))
        else:
            self.font.draw(370, 750, f'frame: {self.t_turn + 1:d}', (0, 0, 0))
        # 바운드 박스
        # draw_rectangle(*self.get_bb_r())
        # draw_rectangle(*self.get_bb_c_1())
        # draw_rectangle(*self.get_bb_c_2())
        # draw_rectangle(*self.get_bb_c_3())
        # draw_rectangle(*self.get_bb_c_4())
        # draw_rectangle(*self.get_bb_c_5())
        # draw_rectangle(*self.get_bb_c_6())

    def get_bb_r(self):
        return self.x - self.bb - 10, self.y - self.bb, self.x + self.bb + 10, self.y + self.bb + 20

    def get_bb_c_1(self):
        if self.giant == 1:
            return self.x - 22, self.y - 2, self.x + 22, self.y + 64
        else:
            return self.x - 12, self.y + 2, self.x + 12, self.y + 54

    def get_bb_c_2(self):
        if self.giant == 1:
            return self.x - 25, self.y - 5, self.x + 25, self.y + 61
        else:
            return self.x - 15, self.y + 5, self.x + 15, self.y + 51

    def get_bb_c_3(self):
        if self.giant == 1:
            return self.x - 28, self.y - 8, self.x + 28, self.y + 58
        else:
            return self.x - 18, self.y + 8, self.x + 18, self.y + 48

    def get_bb_c_4(self):
        if self.giant == 1:
            return self.x - 31, self.y + 1, self.x + 31, self.y + 55
        else:
            return self.x - 21, self.y + 11, self.x + 21, self.y + 45

    def get_bb_c_5(self):
        if self.giant == 1:
            return self.x - 34, self.y + 3, self.x + 34, self.y + 52
        else:
            return self.x - 24, self.y + 13, self.x + 24, self.y + 42

    def get_bb_c_6(self):
        if self.giant == 1:
            return self.x - 37, self.y + 7, self.x + 37, self.y + 49
        else:
            return self.x - 27, self.y + 17, self.x + 27, self.y + 39

    def handle_collision_r(self, group, other):
        # 사각형과 사각형 충돌
        if group == 'bottle:potato(r)':
            pass

    def handle_collision_c(self, group, other):
        # 사각형과 원 충돌
        if group == 'bottle:potato(c)':
            pass

    def reset_potato(self):
        # 감자 속성 초기화
        # 위치
        self.x = 270
        self.y = 100
        # 크기
        self.size = 150
        # 스핀
        self.spin = 0
        # 힘
        self.power = 0
        # 속도
        self.speed = 5
        # 능력
        self.giant = 0
        # 충돌범위
        self.bb = 0
        # 각도
        self.angle = 0
        # dir
        self.dir = 1
        # 현재 플레이어의 턴을 -1
        self.turn -= 1
        # 충돌 ok
        self.collision_ok = 0
        # 현재 상태
        self.state_machine.cur_state = Idle
        # 턴 종료
        if self.turn <= 0 or self.p1_f1_score + self.p1_f2_score == 10 or self.p2_f1_score + self.p2_f2_score == 10:
            # 점수 계산
            # 스트라이크
            if self.turn == 1:
                self.total_score(2)
            # 스페어
            elif self.turn == 0 and self.p1_f1_score + self.p1_f2_score == 10:
                # last frame에서 다 쓰러뜨리면 스트라이크 처리
                if self.t_turn == 10:
                    self.total_score(2)
                else:
                    self.total_score(1)
            # 스페어
            elif self.turn == 0 and self.p2_f1_score + self.p2_f2_score == 10:
                # last frame에서 다 쓰러뜨리면 스트라이크 처리
                if self.t_turn == 10:
                    self.total_score(2)
                else:
                    self.total_score(1)
            else:
                self.total_score(0)
            # 플레이어 변경
            if self.player == 0:
                self.p1_save_f1_score.append(self.p1_f1_score)
                self.p1_save_f2_score.append(self.p1_f2_score)
                self.p1_save_f_score.append(self.p1_t_score)
                self.p1_f1_score = 0
                self.p1_f2_score = 0
                self.player = 1
            else:
                self.p2_save_f1_score.append(self.p2_f1_score)
                self.p2_save_f2_score.append(self.p2_f2_score)
                self.p2_save_f_score.append(self.p2_t_score)
                self.p2_f1_score = 0
                self.p2_f2_score = 0
                self.player = 0
                # 게임의 턴을 증가
                self.t_turn += 1
                print('--------')
                print('Frame', self.t_turn + 1)
            # 턴 개수 회복
            if self.t_turn != 10:
                self.turn = 2
            else:
                self.turn = 1
            # next_state 활성화
            play_mode.next_stage()

    def total_score(self, type):
        # 점수 계산
        if self.player == 0:  # p1
            if type == 2:  # 스트라이크
                self.p1_t_score += 10 + self.p1_f1_score + self.p1_f2_score
                self.p1_ss.append(2)
                print('p1_f1: strike')
                print('p1_f2: strike')
            elif type == 1:  # 스페어
                self.p1_t_score += 10 + self.p1_f1_score
                self.p1_ss.append(1)
                print('p1_f1: ', self.p1_f1_score)
                print('p1_f2: spare')
            else:  # 일반
                self.p1_t_score += self.p1_f1_score + self.p1_f2_score
                self.p1_ss.append(0)
                print('p1_f1: ', self.p1_f1_score)
                print('p1_f2: ', self.p1_f2_score)
            print('p1_t : ', self.p1_t_score)
        elif self.player == 1:  # p2
            if type == 2:  # 스트라이크
                self.p2_t_score += 10 + self.p2_f1_score + self.p2_f2_score
                self.p2_ss.append(2)
                print('p2_f1: strike')
                print('p2_f2: strike')
            elif type == 1:  # 스페어
                self.p2_t_score += 10 + self.p2_f1_score
                self.p2_ss.append(1)
                print('p2_f1: ', self.p2_f1_score)
                print('p2_f2: spare')
            else:  # 일반
                self.p2_t_score += self.p2_f1_score + self.p2_f2_score
                self.p2_ss.append(0)
                print('p2_f1: ', self.p2_f1_score)
                print('p2_f2: ', self.p2_f2_score)
            print('p2_t : ', self.p2_t_score)
