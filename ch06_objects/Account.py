import os
import pickle
import tempfile
from datetime import datetime


class AccountError(Exception):
    pass


class NoFilenameError(AccountError):
    pass


class SaveError(AccountError):
    pass


class LoadError(AccountError):
    pass


class Account:
    """Account store info about account number, name and list of Transactions
    """

    def __init__(self, number, name):
        if number is None:
            raise ValueError('number should be provided')
        self._verify_name(name)
        self._number = number
        self._name = name
        self._transactions = []

    def _verify_name(self, name):
        if name is None:
            raise ValueError('name should be provided')
        if len(name) < 4:
            raise ValueError('name should be at least 4 characters')

    @property
    def number(self):
        """
        >>> acc = Account(1, 'account')
        >>> acc.number
        1
        >>> acc.number = 100
        Traceback (most recent call last):
        ...
        AttributeError: can't set attribute
        """
        return self._number

    @property
    def name(self):
        """
        >>> acc = Account(1, 'new account')
        >>> acc.name
        'new account'
        >>> acc.name = 'updated account'
        >>> acc.name
        'updated account'
        >>> acc.name = 'acc'
        Traceback (most recent call last):
        ...
        ValueError: name should be at least 4 characters
        """
        return self._name

    @name.setter
    def name(self, name):
        self._verify_name(name)
        self._name = name

    def apply(self, transaction):
        if transaction is None:
            raise ValueError('transaction should be provided')
        self._transactions.append(transaction)

    def __len__(self):
        return len(self._transactions)

    @property
    def balance(self):
        """Return balance in USD for all account transactions

        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> acc = Account(42, 'default')
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.balance
        100.0

        >>> acc.apply(Transaction(6250, timestamp, currency='RUB', usd_conversion_rate=62.5))
        >>> acc.balance
        200.0
        """
        balance = 0
        for t in self._transactions:
            balance += t.usd
        return balance

    @property
    def all_usd(self):
        """Return balance in USD for all account transactions

        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> acc = Account(42, 'default')
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.all_usd
        True

        >>> acc.apply(Transaction(6250, timestamp, currency='RUB', usd_conversion_rate=62.5))
        >>> acc.all_usd
        False
        """
        for t in self._transactions:
            if t.currency != 'USD':
                return False
        return True

    def save(self, filename=None):
        """Save Account state in pickle format

        >>> account_name = 'default'
        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> acc = Account(42, account_name)
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.apply(Transaction(6250, timestamp, currency='RUB', usd_conversion_rate=62.5))

        >>> tmp_dir = tempfile.gettempdir()
        >>> dump_filename = os.path.join(tmp_dir, account_name)
        >>> dump_full_filename = dump_filename + '.acc'

        >>> acc.save(dump_full_filename)
        >>> os.path.exists(dump_full_filename)
        True

        >>> os.remove(dump_full_filename)

        >>> acc.save(dump_filename )
        >>> os.path.exists(dump_full_filename)
        True

        >>> os.remove(dump_full_filename)

        >>> acc.save()
        >>> os.path.exists(dump_filename + '.acc')
        True
        """
        if filename is not None:
            self.filename = filename
        if self.filename is None:
            raise NoFilenameError(filename)

        if not self.filename.endswith('.acc'):
            self.filename += '.acc'

        fd = None
        try:
            fd = open(self.filename, 'wb')
            data = (self._name, self._number, self._transactions)
            pickle.dump(data, fd, pickle.HIGHEST_PROTOCOL)
        except (EnvironmentError, pickle.PicklingError) as err:
            raise SaveError(err)
        finally:
            if fd is not None:
                fd.close()

    def load(self, filename=None):
        """Load Account state from pickle format

        >>> account_name = 'default'
        >>> timestamp = datetime(2019, 5, 19, 22, 20, 0)
        >>> acc = Account(42, account_name)
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.apply(Transaction(100, timestamp))
        >>> acc.apply(Transaction(6250, timestamp, currency='RUB', usd_conversion_rate=62.5))
        >>> tmp_dir = tempfile.gettempdir()
        >>> dump_full_filename = os.path.join(tmp_dir, account_name) + '.acc'
        >>> acc.save(dump_full_filename)

        >>> acc = Account(112, 'new name')
        >>> acc.load(dump_full_filename)
        >>> acc.name
        'default'
        >>> acc.number
        42
        """
        if filename is not None:
            self.filename = filename
        if self.filename is None:
            raise NoFilenameError(filename)

        if not self.filename.endswith('.acc'):
            self.filename += '.acc'

        fd = None
        try:
            fd = open(self.filename, 'rb')
            (name, number, transactions) = pickle.load(fd)
            self.name = name
            self._number = number
            self._transactions = transactions
        except (EnvironmentError, pickle.PicklingError) as err:
            raise LoadError(err)
        finally:
            if fd is not None:
                fd.close()


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


if __name__ == '__main__':
    import doctest

    doctest.testmod()
