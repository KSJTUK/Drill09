from pico2d import load_image


# 원래 객체를 만드는 이유는 객체를 찍어내기 위해서이다
# 파이썬에서는 객체 생성용이아닌 여러개의 함수를 모아 그룹으로 관리하는 기능이 있다.
class IDLE:

    @staticmethod
    def enter():
        print("IDLE Entered")
        pass

    @staticmethod
    def exit():
        print("IDLE Exit")
        pass

    @staticmethod
    def do():
        print("IDLE Do")
        pass


class StateMachine:
    def __init__(self):
        self.cur_state = IDLE

    def start(self):
        self.cur_state.enter()

    def update(self):
        self.cur_state.do()

    def draw(self):
        pass


class Boy:
    def __init__(self):
        self.x, self.y = 400, 90
        self.frame = 0
        self.dir = 0
        self.action = 3
        self.image = load_image('animation_sheet.png')
        self.state_machine = StateMachine()
        self.state_machine.start()

    def update(self):
        self.frame = (self.frame + 1) % 8
        self.state_machine.update()

    def handle_event(self, event):
        pass

    def draw(self):
        self.image.clip_draw(self.frame * 100, self.action * 100, 100, 100, self.x, self.y)
        self.state_machine.draw()
