from pico2d import load_image


# 원래 객체를 만드는 이유는 객체를 찍어내기 위해서이다
# 파이썬에서는 객체 생성용이아닌 여러개의 함수를 모아 그룹으로 관리하는 기능이 있다.
class IDLE:
    @staticmethod
    def enter(boy):
        print("IDLE Entered")
        pass

    @staticmethod
    def exit(boy):
        print("IDLE Exit")
        pass

    @staticmethod
    def do(boy):
        print("IDLE Do")
        pass

    @staticmethod
    def draw(boy):
        boy.image.clip_draw(boy.frame * 100, boy.action * 100, 100, 100,
                             boy.x, boy.y)
        pass


class StateMachine:
    def __init__(self, boy):
        self.boy = boy
        self.cur_state = IDLE

    def start(self):
        self.cur_state.enter(self.boy)

    def update(self):
        self.cur_state.do(self.boy)

    def draw(self):
        self.cur_state.draw(self.boy)
        pass


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
        pass

    def draw(self):
        self.state_machine.draw()
