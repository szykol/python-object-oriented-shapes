from Shapes import *

# t = Triangle((10, 10, 10))
# print(t.area())

c = ConvexQuadrilateral(100, 100, 120, 0.5, 0.5)
if (c.perimeter() == 4 * 5 * math.sqrt(2)):
    print('correct perimeter')

if (c.area() == 50):
    print('correct area')

c.draw()