import descriptors as de
import abc
import numbers

class ConvexPolygon(abc.ABC):
    @abc.abstractclassmethod
    def __init__(self):
        self.fill_color = None
        self.outline_color = None

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
    def __init__(self):
        self.a = de.QuantityAndType(numbers.Real)
        self.b = de.QuantityAndType(numbers.Real)
        self.c = de.QuantityAndType(numbers.Real)
        
        super().__init__()

    def draw(self):
        pass
    
    def perimeter(self):
        pass

    def area(self):
        pass