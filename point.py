from pico2d import load_image


class Point:
    def __init__(self, x=140, y=500):
        self.image = load_image('Resource\\UI\\icon_3_3.png')
        self.x, self.y = x, y
        self.dir = 0

    def draw(self):
        self.image.draw_to_origin(self.x, self.y, 100, 100)

    def update(self):
        pass
