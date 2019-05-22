from datetime import datetime


class Transaction:
    """Transaction store info about currency transaction
    and calculate amount in USD (based on usd_conversion_rate)

    usd_conversion_rate for USD must always be equal to 1.0
    """

    def __init__(self, amount, date, currency='USD', usd_conversion_rate=1.0,
                 description=None):
        """
        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> str(Transaction(1, timestamp, currency='USD'))
        '1 USD at 2019-05-19 22:20:00'
        >>> Transaction(1, timestamp, currency='USD', usd_conversion_rate=10.0)
        Traceback (most recent call last):
        ...
        ValueError: USD conversion rate should be equal to 1.0
        >>> str(Transaction(1, timestamp, currency='EUR', usd_conversion_rate=1.0))
        '1 EUR at 2019-05-19 22:20:00'
        >>> Transaction(None, timestamp)
        Traceback (most recent call last):
        ...
        ValueError: amount could not be None
        >>> Transaction(1, None)
        Traceback (most recent call last):
        ...
        ValueError: date could not be None
        """
        if amount is None:
            raise ValueError('amount could not be None')
        if date is None:
            raise ValueError('date could not be None')
        if currency == 'USD' and not usd_conversion_rate == 1.0:
            raise ValueError('USD conversion rate should be equal to 1.0')
        self._amount = amount
        self._date = date
        self._currency = currency
        self._usd_conversion_rate = usd_conversion_rate
        self._description = description

    @property
    def amount(self):
        return self._amount

    @property
    def date(self):
        return self._date

    @property
    def currency(self):
        return self._currency

    @property
    def usd_conversion_rate(self):
        return self._usd_conversion_rate

    @property
    def description(self):
        return self._description

    @property
    def usd(self):
        """Return calculated amount in USD

        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> t = Transaction(1, timestamp)
        >>> t.usd
        1.0
        >>> t = Transaction(6250, timestamp, currency='RUB', usd_conversion_rate=62.5)
        >>> t.usd
        100.0
        """
        return self._amount / self._usd_conversion_rate

    def __str__(self):
        return '{0} {1} at {2}'.format(
            self._amount, self._currency, self._date
        )

    def __repr__(self):
        return ("{0}(amount={1}, date={2}, currency={3}, "
                "usd_conversion_rate={4}, description={5})").format(
            self.__class__.__name__,
            self._amount, repr(self._date), self._currency,
            self._usd_conversion_rate, repr(self._description)
        )
