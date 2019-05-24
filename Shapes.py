import descriptors as de
import abc
import numbers
import math
from colors import Color

class ConvexPolygon(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self):
        self.fill_color = Color.BLACK
        self.outline_color = Color.WHITE

    @abc.abstractclassmethod
    def area(self):
        pass

    @abc.abstractclassmethod
    def perimeter(self):
        pass

    @abc.abstractclassmethod
    def draw(self):
        pass


class Triangle(ConvexPolygon):
    a = de.QuantityAndType(numbers.Real)
    b = de.QuantityAndType(numbers.Real)
    c = de.QuantityAndType(numbers.Real)

    def __init__(self, sides):
        self.a, self.b, self.c = sides
        super().__init__()

    def draw(self):
        pass

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        return self.a * self.b / 2


class ConvexQuadrilateral(ConvexPolygon):
    a = de.QuantityAndType(numbers.Real)
    b = de.QuantityAndType(numbers.Real)
    c = de.QuantityAndType(numbers.Real)
    d = de.QuantityAndType(numbers.Real)

    def __init__(self, sides):
        self.a, self.b, self.c, self.d = sides
        super().__init__()

    def draw(self):
        pass

    def perimeter(self):
        return self.a + self.b + self.c + self.d

    def area(self):
        return self.a * self.b / 2


class RegularPolygon(ConvexPolygon):
    side = de.QuantityAndType(numbers.Real)
    side_count = de.QuantityAndType(int)

    def __init__(self, side_count):
        self.side_count = side_count
        super().__init__()

    def draw(self):
        pass

    def perimeter(self):
        return self.side * self.side_count

    def area(self):
        return self.side ** 2 * self.side_count / 4 * math.tan(math.radians(180 / self.side_count))


class RegularHexagon(RegularPolygon):
    def __init__(self):
        return super().__init__(6)


class RegularPentagon(RegularPolygon):
    def __init__(self):
        return super().__init__(5)


class RegularOctagon(RegularPolygon):
    def __init__(self):
        return super().__init__(8)


class IsoscelesTriangle(Triangle):
    def __init__(self, ramie, podst):
        return super().__init__((ramie, ramie, podst))


class EquilateralTriangle(Triangle):
    def __init__(self, side):
        return super().__init__((side) * 3)


class Parallelogram(ConvexQuadrilateral):
    def __init__(self, a, b):
        return super().__init__((a, b, a, b))


class Kite(ConvexQuadrilateral):
    def __init__(self, a, b):
        return super().__init__((a, a, b, b))


class Rhombus(Parallelogram):
    def __init__(self, a):
        return super().__init__((a, a))


class Square(Parallelogram):
    def __init__(self, a, b):
        return super().__init__((a, a))
