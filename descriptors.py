import abc

# deskryptor - zapewnia większą funkcjonalność
class AutoStorage:
    _count = 0
    def __init__(self):
        cls = self.__class__ 
        prefix = cls.__name__
        index = cls._count
        self.storage_name = f'_{prefix}#{index}'
        cls._count += 1

    def __get__(self, instance, owner):
        # jeżeli wywołanie nie nastąpi przez instancję zwraca sam deskryptor
        # w przeciwnym wypadku zwróć wartość atrybutu zarządzanego
        if instance is None:
            return self
        else:
            return getattr(instance, self.storage_name)

    def __set__(self, instance, value):
        # sprawdzaniem poprawność jest odelegowane do klasy Validated
        # (a właściwie do klas po niej dzidziczących)
        setattr(instance, self.storage_name, value)


# klasa abstarkcyjna ale dziedziczy po AutoStorage
class Validated(abc.ABC, AutoStorage):
    # __set__ deleguje sprawdzanie poprawności do meotody validate
    def __set__(self, instance, value):
        value = self.validate(instance, value)
        super().__set__(instance, value) # wywołanie metody klasy nadrzędnej (faktyczny zapis danych)

    @abc.abstractmethod
    def validate(self, instance, value):
        """Zwraca zweryfikowaną wartość lub zgłasza wyjątek ValueError"""


class Quantity(Validated):
    """sprawdza czy liczba jest większa od zera"""
    def validate(self, instance, value):
        if value >0:
            return value
        else:
            raise ValueError("wartość musi być większa od zera!")

class QuantityAndType(Validated):
    """sprawdza czy liczba jest większa od zera
       i czy typ się zgadza
    """

    def __init__(self, data_type=None):
        self.type = data_type

    def validate(self, instance, value):
        if value >0 and self.type is not None and isinstance(value, self.type):
            return value
        elif self.type is not None:
            raise ValueError("wartość musi być większa od zera i być typu {}!".format(self.type))

class NonBlank(Validated):
    """sprawdza czy ciąg tekstowy jest niepusty"""
    def validate(self, instance, value):
        if len(value.strip()) > 0:
            return value
        else:
            raise ValueError("wartość musi niepustym ciągiem tekstowym")    

