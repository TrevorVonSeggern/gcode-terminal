from .abstractions import IMainUi, IScreen

class MainUi(IMainUi):
    def __init__(self, screen: IScreen):
        self.status = screen.statusLine()
        (left, right) = screen.splitLeftRight()
        self.left = left
        self.right = right
