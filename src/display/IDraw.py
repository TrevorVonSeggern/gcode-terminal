from abc import ABC, abstractmethod
from display.point import Point

class IDraw(ABC):
    @abstractmethod
    def draw(self, content: str, point: Point):
        pass
