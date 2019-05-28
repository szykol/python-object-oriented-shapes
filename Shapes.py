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

        self._calc_angles()
        super().__init__()

    def draw(self):
        A = Point(300, 300)
        S = apply_vect(A, Vect(self.AS, 0))
        B = apply_vect(S, Vect(self.BS, math.radians(180 - self.ASB_angle)))
        C = apply_vect(S, Vect(self.CS, 0))
        D = apply_vect(S, Vect(self.DS, math.radians(180 + self.ASD_angle)))

        master = Tk()

        w = Canvas(master, width=800, height=800)
        w.pack()

        w.create_polygon([A,B,C,D], fill=self.fill_color, outline=self.outline_color)        
        mainloop()


    def perimeter(self):
        AB = self.AS ** 2 + self.BS ** 2 - 2 * self.AS * self.BS * math.cos(math.radians(self.ASB_angle))
        AB = math.sqrt(AB)
        BC = self.BS ** 2 + self.CS ** 2 - 2 * self.BS * self.CS * math.cos(math.radians(self.BSC_angle))
        BC = math.sqrt(BC)
        CD = self.CS ** 2 + self.DS ** 2 - 2 * self.CS * self.DS * math.cos(math.radians(self.DSC_angle))
        CD = math.sqrt(CD)
        DA = self.DS ** 2 + self.AS ** 2 - 2 * self.DS * self.AS * math.cos(math.radians(self.ASD_angle))
        DA = math.sqrt(DA)

        return AB + BC + CD + DA
 
    def area(self):
        ASB_area = self.AS * self.BS / 2 * math.sin(math.radians(self.ASB_angle))
        BSC_area = self.CS * self.BS / 2 * math.sin(math.radians(self.BSC_angle))
        ASD_area = self.AS * self.DS / 2 * math.sin(math.radians(self.ASD_angle))
        DSC_area = self.CS * self.DS / 2 * math.sin(math.radians(self.DSC_angle))

        return ASB_area + BSC_area + ASD_area + DSC_area
    
    def _calc_angles(self):
        self.AS = self.BD_cuts_AC_ratio * self.AC_diagonal
        self.CS = self.AC_diagonal - self.AS

        self.BS = self.AC_cuts_BD_ratio * self.BD_diagonal
        self.DS = self.BD_diagonal - self.BS

        self.ASD_angle = self.BSC_angle = 180 - self.ASB_angle
        self.DSC_angle = self.ASB_angle

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
