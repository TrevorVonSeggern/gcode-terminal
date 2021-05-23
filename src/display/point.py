from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Point:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def OnlyX(self) -> Point:
        return Point(self.x, 0)

    def OnlyY(self) -> Point:
        return Point(0, self.y)

    def Deconstruct(self) -> (int, int):
        return (self.x, self.y)

    def __add__(self, other) -> Point:
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self) -> str:
        return '({0}, {1})'.format(self.x, self.y)

Point.Zero = Point(0, 0)
Point.One = Point(1, 1)
