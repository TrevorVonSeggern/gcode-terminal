import unittest
from unittest.mock import Mock
from src.display.point import Point
from src.display.window import Window

class TestPoint(unittest.TestCase):
    def test_draw(self):
        # Given
        display = Mock()
        window = Window(Point.Zero, 10, 10, display)

        # When
        window.draw('hello world', Point.Zero)

        # Then
        display.draw.assert_called_once()

    def test_draw_pointHasOffset(self):
        # Given
        display = Mock()
        window = Window(Point.One, 10, 10, display)

        # When
        window.draw('hello world', Point.Zero)

        # Then
        display.draw.assert_called_once_with('hello world', Point.One)

    def test_write_callsDraw(self):
        # given
        display = Mock()
        window = Window(Point.One, 10, 10, display)

        # When
        window.writeLine('hi')

        # Then
        display.draw.assert_called_once()

    def test_write_None_doesNotCallDraw(self):
        # Given
        display = Mock()
        window = Window(Point.One, 10, 10, display)

        # When
        window.writeLine(None)

        # Then
        display.draw.assert_not_called()

if __name__ == '__main__':
    unittest.main()
