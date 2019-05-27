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
    AC_diagonal = de.QuantityAndType(numbers.Real)
    BD_diagonal = de.QuantityAndType(numbers.Real)

    # angle = de.Range(0, math.pi / 2)
    angle = de.Range(0, 180)

    AC_cuts_BD_ratio = de.Range(0, 1)
    BD_cuts_AC_ratio = de.Range(0, 1)

    def __init__(self, a_diagon, b_diagon, angle, AC_ratio, BD_ratio):
        self.AC_diagonal = a_diagon
        self.BD_diagonal = b_diagon

        self.ASB_angle = angle
        self.AC_cuts_BD_ratio = AC_ratio
        self.BD_cuts_AC_ratio = BD_ratio
        super().__init__()

    def draw(self):
        pass

    def perimeter(self):
        AS = self.BD_cuts_AC_ratio * self.AC_diagonal
        CS = self.AC_diagonal - AS

        BS = self.AC_cuts_BD_ratio * self.BD_diagonal
        DS = self.BD_diagonal - BS

        ASD_angle = BSC_angle = 180 - self.ASB_angle
        DSC_angle = self.ASB_angle

        AB = AS ** 2 + BS ** 2 - 2 * AS * BS * math.cos(math.radians(self.ASB_angle))
        AB = math.sqrt(AB)
        BC = BS ** 2 + CS ** 2 - 2 * BS * CS * math.cos(math.radians(BSC_angle))
        BC = math.sqrt(BC)
        CD = CS ** 2 + DS ** 2 - 2 * CS * DS * math.cos(math.radians(DSC_angle))
        CD = math.sqrt(CD)
        DA = DS ** 2 + AS ** 2 - 2 * DS * AS * math.cos(math.radians(ASD_angle))
        DA = math.sqrt(DA)

        return AB + BC + CD + DA
 
    def area(self):
        AS = self.BD_cuts_AC_ratio * self.AC_diagonal
        CS = self.AC_diagonal - AS

        BS = self.AC_cuts_BD_ratio * self.BD_diagonal
        DS = self.BD_diagonal - BS

        ASD_angle = BSC_angle = 180 - self.ASB_angle
        DSC_angle = self.ASB_angle

        ASB_area = AS * BS / 2 * math.sin(math.radians(self.ASB_angle))
        BSC_area = CS * BS / 2 * math.sin(math.radians(BSC_angle))
        ASD_area = AS * DS / 2 * math.sin(math.radians(ASD_angle))
        DSC_area = CS * DS / 2 * math.sin(math.radians(DSC_angle))

        return ASB_area + BSC_area + ASD_area + DSC_area

class RegularPolygon(ConvexPolygon):
    side = de.QuantityAndType(numbers.Real)
    side_count = de.QuantityAndType(int)

    def __init__(self, side, side_count):
        self.side_count = side_count
        self.side = side
        super().__init__()

    def draw(self):
        angle = (self.side_count - 2) / self.side_count * 180
        print(angle)
        angle = math.radians(angle)
        vertices = []
        point = Point(300, 100)

        r = self.side
        ang = 360 / self.side_count
        for i in range(self.side_count):
            vertices.append(Point(
                point[0] + r * math.cos(i * ang * math.pi / 180),
                point[1] + r * math.sin(i * ang * math.pi / 180)
            ))

        
        master = Tk()

        w = Canvas(master, width=800, height=800)
        w.pack()

        w.create_polygon(vertices, fill=self.fill_color, outline=self.outline_color)        
        mainloop()

    def perimeter(self):
        return self.side * self.side_count

    def area(self):
        return self.side ** 2 * self.side_count / 4 * math.tan(math.radians(180 / self.side_count))


class RegularHexagon(RegularPolygon):
    def __init__(self, side_len):
        super().__init__(side_len, 6)


class RegularPentagon(RegularPolygon):
    def __init__(self, side_len):
        super().__init__(side_len, 5)


class RegularOctagon(RegularPolygon):
    def __init__(self, side_len):
        super().__init__(side_len, 8)


class IsoscelesTriangle(Triangle):
    def __init__(self, ramie, podst):
        return super().__init__((ramie, podst, ramie))


class EquilateralTriangle(Triangle):
    def __init__(self, side):
        return super().__init__(tuple([side] * 3))


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
