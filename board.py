from pico2d import load_image


class Board:
    def __init__(self, x=0, y=500):
        self.image = load_image('Resource\\UI\\score_board.png')
        self.x, self.y = x, y
        self.dir = 0

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 600, 100)

    def update(self):
        pass
