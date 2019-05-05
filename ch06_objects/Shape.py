import math


class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def distance_from_origin(self):
        return math.hypot(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point({0.x!r}, {0.y!r})".format(self)

    def __str__(self):
        return "({0.x!r}, {0.y!r})".format(self)

    def __add__(self, other):
        """
        >>> q = Point(1, 5)
        >>> r = Point(2, 10)
        >>> p = q + r
        >>> p
        Point(3, 15)
        >>> q = Point(1, 5)
        >>> r = Point(2, -10)
        >>> p = q + r
        >>> p
        Point(3, -5)
        """
        return Point(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        """
        >>> p = Point(1, 5)
        >>> q = Point(2, 10)
        >>> p += q
        >>> p
        Point(3, 15)
        >>> p = Point(1, 5)
        >>> q = Point(2, -10)
        >>> p += q
        >>> p
        Point(3, -5)
        """
        self.x = self.x + other.x
        self.y = self.y + other.y
        return self

    def __sub__(self, other):
        """
        >>> q = Point(1, 5)
        >>> r = Point(2, 10)
        >>> p = q - r
        >>> p
        Point(-1, -5)
        >>> q = Point(1, 5)
        >>> r = Point(2, -10)
        >>> p = q - r
        >>> p
        Point(-1, 15)
        """
        return Point(self.x - other.x, self.y - other.y)

    def __isub__(self, other):
        """
        >>> p = Point(1, 5)
        >>> q = Point(2, 10)
        >>> p -= q
        >>> p
        Point(-1, -5)
        >>> p = Point(1, 5)
        >>> q = Point(2, -10)
        >>> p -= q
        >>> p
        Point(-1, 15)
        """
        self.x = self.x - other.x
        self.y = self.y - other.y
        return self

    def __mul__(self, number):
        """
        >>> q = Point(1, 5)
        >>> n = 2
        >>> p = q * n
        >>> p
        Point(2, 10)
        >>> q = Point(-1, 5)
        >>> n = -2
        >>> p = q * n
        >>> p
        Point(2, -10)
        """
        return Point(self.x * number, self.y * number)

    def __imul__(self, number):
        """
        >>> p = Point(1, 5)
        >>> n = 2
        >>> p *= n
        >>> p
        Point(2, 10)
        >>> p = Point(-1, 5)
        >>> n = -2
        >>> p *= n
        >>> p
        Point(2, -10)
        """
        self.x = self.x * number
        self.y = self.y * number
        return self

    def __truediv__(self, number):
        """
        >>> q = Point(1, 5)
        >>> n = 2
        >>> p = q / n
        >>> p
        Point(0.5, 2.5)
        >>> q = Point(-2, -10)
        >>> n = 2
        >>> p = q / n
        >>> p
        Point(-1.0, -5.0)
        """
        return Point(self.x / number, self.y / number)

    def __itruediv__(self, number):
        """
        >>> p = Point(1, 5)
        >>> n = 2
        >>> p /= n
        >>> p
        Point(0.5, 2.5)
        >>> p = Point(-2, -10)
        >>> n = 2
        >>> p /= n
        >>> p
        Point(-1.0, -5.0)
        """
        self.x = self.x / number
        self.y = self.y / number
        return self

    def __floordiv__(self, number):
        """
        >>> q = Point(1, 5)
        >>> n = 2
        >>> p = q // n
        >>> p
        Point(0, 2)
        >>> q = Point(-2, -10)
        >>> n = 2
        >>> p = q // n
        >>> p
        Point(-1, -5)
        """
        return Point(self.x // number, self.y // number)

    def __ifloordiv__(self, number):
        """
        >>> p = Point(1, 5)
        >>> n = 2
        >>> p //= n
        >>> p
        Point(0, 2)
        >>> p = Point(-2, -10)
        >>> n = 2
        >>> p //= n
        >>> p
        Point(-1, -5)
        """
        self.x = self.x // number
        self.y = self.y // number
        return self


class Circle(Point):
    def __init__(self, radius, x=0, y=0):
        super().__init__(x, y)
        self.radius = radius

    @property
    def radius(self):
        """The circle's radius

        >>> circle = Circle(-2)
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle = Circle(4)
        >>> circle.radius = -1
        Traceback (most recent call last):
        ...
        AssertionError: radius must be nonzero and non-negative
        >>> circle.radius = 6
        """
        return self.__radius

    @radius.setter
    def radius(self, radius):
        assert radius > 0, "radius must be nonzero and non-negative"
        self.__radius = radius

    def edge_distance_from_origin(self):
        return abs(self.distance_from_origin() - self.radius)

    def area(self):
        return math.pi * (self.radius ** 2)

    def circumference(self):
        return 2 * math.pi * self.radius

    def __eq__(self, other):
        return self.radius == other.radius and super().__eq__(other)

    def __repr__(self):
        return "Circle({0.radius!r}, {0.x!r}, {0.y!r})".format(self)

    def __str__(self):
        return repr(self)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
