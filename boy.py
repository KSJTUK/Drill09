from pico2d import load_image, SDL_KEYDOWN, SDL_KEYUP, get_canvas_height, get_canvas_width, \
    SDLK_SPACE, get_time, \
    SDLK_RIGHT, SDLK_LEFT, SDLK_a
import math


def key_a_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_a


def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE


def time_out(e):
    return e[0] == 'TIME_OUT'


# 원래 객체를 만드는 이유는 객체를 찍어내기 위해서이다
# 파이썬에서는 객체 생성용이아닌 여러개의 함수를 모아 그룹으로 관리하는 기능이 있다.
class IDLE:
    @staticmethod
    def enter(boy, e):
        if boy.action == 0:
            boy.action = 2
        elif boy.action == 1:
            boy.action = 3
        boy.dir = 0
        boy.frame = 0
        boy.idle_start_time = get_time()

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        if get_time() - boy.idle_start_time > 3:
            boy.state_machine.handle_event(('TIME_OUT', 0))

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                            boy.x, boy.y)


class Run:
    @staticmethod
    def enter(boy, e):
        if right_down(e) or left_up(e):
            boy.dir, boy.action = 1, 1
        elif left_down(e) or right_up(e):
            boy.dir, boy.action = -1, 0

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 5

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100, boy.x, boy.y)


class AutoRun:
    @staticmethod
    def enter(boy, e):
        if boy.action == 2:  # 캐릭터가 왼쪽을 바라보고있으면
            boy.dir, boy.action = -1, 0  # 왼쪽으로 움직임
        elif boy.action == 3:  # 캐릭터가 오른쪽을 바라보고있으면
            boy.dir, boy.action = 1, 1  # 오른쪽으로 움직임
        boy.auto_run_start_time = get_time()  # AutoRun 상태 시작 시간 설정

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8
        boy.x += boy.dir * 30

        canvas_width = get_canvas_width()

        if boy.x > canvas_width - 15:
            boy.x = canvas_width - 15
            boy.dir, boy.action = -1, 0
        elif boy.x < 15:
            boy.x = 15
            boy.dir, boy.action = 1, 1

        if get_time() - boy.auto_run_start_time > 5:  # 5초가 지나면
            boy.state_machine.handle_event(('TIME_OUT', 0))  # TIME_OUT 이벤트를 발생시킨다

    @staticmethod
    def draw(boy):
        boy.image.clip_composite_draw(boy.frame * 100, boy.action * 100, 100, 100,
                                      0, ' ', boy.x, boy.y + 20, 150, 150)


class Sleep:
    @staticmethod
    def enter(boy, e):
        boy.frame = 0
        pass

    @staticmethod
    def exit(boy, e):
        pass

    @staticmethod
    def do(boy):
        boy.frame = (boy.frame + 1) % 8

    @staticmethod
    def draw(boy):
        if boy.action == 2:
            boy.image.clip_composite_draw(boy.frame * 100, 200, 100, 100,
                                          -math.pi / 2, ' ', boy.x + 25, boy.y - 25, 100, 100)
        else:
            boy.image.clip_composite_draw(boy.frame * 100, 300, 100, 100,
                                          math.pi / 2, ' ', boy.x - 25, boy.y - 25, 100, 100)


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = IDLE
        self.transitions = {
            IDLE: {key_a_down: AutoRun, right_down: Run, left_down: Run, right_up: Run, left_up: Run, time_out: Sleep},
            Run: {right_down: IDLE, left_down: IDLE, right_up: IDLE, left_up: IDLE},
            Sleep: {right_down: Run, left_down: Run, right_up: Run, left_up: Run, space_down: IDLE},
            AutoRun: {time_out: IDLE}
        }

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.boy, e)
                self.cur_state = next_state
                self.cur_state.enter(self.boy, e)
                return True
        return False

    def start(self):
        self.cur_state.enter(self.boy, ('INPUT', 0))

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
