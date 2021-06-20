from abc import ABC, abstractmethod
from display.point import Point

class IDraw(ABC):
    @abstractmethod
    def draw(self, content: str, point: Point):
        pass
    @abstractmethod
    def writeLine(self, line: str):
        pass

class IScreen(IDraw, ABC):
    @abstractmethod
    def splitLeftRight(self) -> (IDraw, IDraw):
        pass

    @abstractmethod
    def statusLine(self) -> (IDraw, IDraw):
        pass

class IWindow(IDraw, ABC):
    @abstractmethod
    def reDraw(self):
        pass

class IMainUI(ABC):
    pass
