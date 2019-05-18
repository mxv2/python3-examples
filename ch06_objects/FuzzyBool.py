class FuzzyBool:
    def __init__(self, value=0.0):
        self.__value = value if 0.0 <= value <= 1.0 else 0.0

    def __eq__(self, other):
        return self.__value == other.value

    def __str__(self):
        """
        >>> f = FuzzyBool(0.5)
        >>> str(f)
        '0.5'
        """
        return str(self.__value)

    def __repr__(self):
        """
        >>> f = FuzzyBool(0.5)
        >>> repr(f)
        'FuzzyBool(0.5)'
        """
        return ("{0}({1})".format(self.__class__.__name__,
                                  self.__value))

    def __format__(self, format_spec):
        """
        >>> f = FuzzyBool(0.509)
        >>> "{0:f}".format(f)
        '0.509'
        >>> "{0:.2f}".format(f)
        '0.51'
        >>> "{0:.1f}".format(f)
        '0.5'
        """
        return self.__value.__format__(format_spec)

    def __bool__(self):
        """
        >>> bool(FuzzyBool(.5))
        False
        >>> bool(FuzzyBool(.75))
        True
        """
        return self.__value > 0.5

    def __int__(self):
        """
        >>> int(FuzzyBool(.5))
        0
        >>> int(FuzzyBool(.75))
        1
        """
        return round(self.__value)

    def __float__(self):
        """
        >>> float(FuzzyBool(.5))
        0.5
        >>> float(FuzzyBool(.75))
        0.75
        """
        return self.__value

    def __hash__(self):
        return hash(id(self))

    def __format__(self, format_spec):
        return super().__format__(format_spec)

    def __invert__(self):
        """
        >>> f = ~FuzzyBool(0.3)
        >>> repr(f)
        'FuzzyBool(0.7)'
        """
        return FuzzyBool(1.0 - self.__value)

    def __and__(self, other):
        """
        >>> f = FuzzyBool(0.3) & FuzzyBool(0.7)
        >>> repr(f)
        'FuzzyBool(0.3)'
        """
        return FuzzyBool(min(self.__value, other.__value))

    def __iand__(self, other):
        """
        >>> f = FuzzyBool(0.7)
        >>> f &= FuzzyBool(0.3)
        >>> repr(f)
        'FuzzyBool(0.3)'
        """
        self.__value = min(self.__value, other.__value)
        return self

    def __or__(self, other):
        """
        >>> f = FuzzyBool(0.3) | FuzzyBool(0.7)
        >>> repr(f)
        'FuzzyBool(0.7)'
        """
        return FuzzyBool(max(self.__value, other.__value))

    def __ior__(self, other):
        """
        >>> f = FuzzyBool(0.3)
        >>> f |= FuzzyBool(0.7)
        >>> repr(f)
        'FuzzyBool(0.7)'
        """
        self.__value = max(self.__value, other.__value)
        return self

    @staticmethod
    def conjunction(*fuzzies):
        """
        >>> f1, f2, f3 = FuzzyBool(0.75), FuzzyBool(0.5), FuzzyBool(0.9)
        >>> str(FuzzyBool.conjunction(f1, f2, f3))
        '0.5'
        """
        return FuzzyBool(min([float(x) for x in fuzzies]))

    @staticmethod
    def disjunction(*fuzzies):
        """
        >>> f1, f2, f3 = FuzzyBool(0.75), FuzzyBool(0.5), FuzzyBool(0.9)
        >>> str(FuzzyBool.disjunction(f1, f2, f3))
        '0.9'
        """
        return FuzzyBool(max([float(x) for x in fuzzies]))


if __name__ == '__main__':
    import doctest

    doctest.testmod()
