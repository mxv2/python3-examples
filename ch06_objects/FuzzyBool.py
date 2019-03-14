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
        return "FuzzyBool({0!r})".format(self.__value)

    def __hash__(self):
        return hash(id(self))

    def __format__(self, format_spec):
        return super().__format__(format_spec)


if __name__ == '__main__':
    import doctest

    doctest.testmod()
