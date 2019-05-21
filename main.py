from Shapes import *

t = Triangle()
try:
    t.a = 'kurwa'
    t.b = -10
    t.c = 10
except ValueError:
    print('error')
else:
    print('good')
    print(t.a)
