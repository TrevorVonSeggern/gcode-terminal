import unittest
from src.display.point import Point

class TestPoint(unittest.TestCase):

    def test_OnlyX(self):
        # Given
        point = Point(10, 11)

        # When
        onlyX = point.OnlyX()

        # Then
        self.assertEqual(onlyX.x, 10)
        self.assertEqual(onlyX.y, 0)

    def test_OnlyY(self):
        # Given
        point = Point(10, 11)

        # When
        onlyY = point.OnlyY()

        # Then
        self.assertEqual(onlyY.x, 0)
        self.assertEqual(onlyY.y, 11)

    def test_Deconstruct(self):
        # Given
        point = Point(10, 11)

        # When
        (x, y) = point.Deconstruct()

        # Then
        self.assertEqual(x, 10)
        self.assertEqual(y, 11)

    def test_Zero(self):
        # Given
        point = Point.Zero

        # When
        (x, y) = point.Deconstruct()

        # Then
        self.assertEqual(x, 0)
        self.assertEqual(y, 0)

    def test_One(self):
        # Given
        point = Point.One

        # When
        (x, y) = point.Deconstruct()

        # Then
        self.assertEqual(x, 1)
        self.assertEqual(y, 1)

if __name__ == '__main__':
    unittest.main()
