import descriptors as de
import abc
import numbers
import math
from colors import Color
from tkinter import *

def Point(x, y):
    return (x, y)

def Vect(len, angle):
    return (len, angle)

def apply_vect(point, vect):
    len, angle = vect
    return Point(point[0] + math.cos(angle) * len, point[1] + math.sin(angle) * len)


class ConvexPolygon(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self):
        self.fill_color = Color.WHITE
        self.outline_color = Color.BLACK

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
        self._calcAngles()
        super().__init__()

    def draw(self):
        master = Tk()

        w = Canvas(master, width=800, height=800)
        w.pack()

        point = (100, 100)
        angle_between = self.alpha
        second_point = apply_vect(point, Vect(self.b, math.radians(angle_between / 2)))
        third_point = apply_vect(second_point, Vect(self.c, math.radians(180 - angle_between / 2)))

        w.create_polygon(*point, *second_point, *third_point, fill=self.fill_color, outline=self.outline_color)        
        mainloop()

    def perimeter(self):
        return self.a + self.b + self.c

    def area(self):
        s = self.perimeter() / 2
        return math.sqrt(s * (s - self.a) * (s - self.b) * (s - self.c))

    def _calcAngles(self):
        def angle (a, b, c):
            return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

        self.alpha = angle(self.a, self.b, self.c)
        print(self.alpha)

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
