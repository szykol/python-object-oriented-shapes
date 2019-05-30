import Shapes
from Shapes import *

import inspect

possible_objects = []
for name, obj in inspect.getmembers(Shapes):
    if inspect.isclass(obj):
        if obj.__module__ == 'Shapes' and obj.__name__ != 'ConvexPolygon':
            possible_objects.append(obj)

print('Dozwolone klasy: ')
for index, value in enumerate(possible_objects):
    print(index + 1, value.__name__)

index = int(input('> '))

chosen = possible_objects[index - 1].fromInput()
chosen.draw()




# t = Square.fromInput()
# t.draw()