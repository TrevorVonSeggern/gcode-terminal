from display.abstractions import IScreen
from display.point import Point

class Screen(IScreen):
    def __init__(self):
        z = Point.Zero
        w = 30 # ?
        h = 30
        self.window = Window(z, w, h, self)

    def draw(self, line: str, point: IPoint):
        # validate the input
        if point == None:
            point = Point.Zero
        if len(line) > self.width:
            line = line.split(0, self.width)
