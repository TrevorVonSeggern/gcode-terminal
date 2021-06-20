from display.abstractions import IMainUi, IScreen

class MainUi(IMainUi):
    def __init__(self, screen: IScreen)
        self.status = Screen.statusLine()
        (left, right) = Screen.splitLeftRight()
        self.left = left
        self.right = right
