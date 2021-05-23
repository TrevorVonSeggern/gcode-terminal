from display.point import Point
from display.IDraw import IDraw

class Window(IDraw):
    def __init__(self, p: Point, w: int, h: int, draw: IDraw):
        self.point = p if p is not None else Point.Zero
        self.width = w if w is not None else 1
        self.height = h if h is not None else 1
        self._draw = draw
        self._lines = []

    def draw(self, content: str, point: Point):
        self._draw.draw(content, self.point + point)

    def writeLine(self, line: str):
        if line == None or str.isspace(line):
            return
        if len(line) > self.width:
            line = line.split(0, self.width)
        self._lines.append(line)
        if len(self._lines) >  self.height:
            self._lines.pop(0)
            self.reDraw()
        else:
            self.draw(line, Point(0, len(self._lines) - 1))

    def reDraw(self):
        pass

    def __repr__(self):
        return 'p:({0},{1}) w:{2}, h:{3}'.format(self.point.x, self.point.y,
                                                 self.width, self.height)
