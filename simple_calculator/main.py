# -*- coding: utf-8 -*-

import operator
from functools import reduce
import numbers


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        if not all(args):
            raise ValueError
        return reduce(operator.mul, args)

    def div(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return float('inf')

    def avg(self, it, lt=None, ut=None):
        count = 0
        total = 0

        for number in it:
            if lt is not None and number < lt:
                continue
            if ut is not None and number > ut:
                continue
            count += 1
            total += number

        if count == 0:
            return 0

        return total / count

    def square(self, n):
        """Return the square of *n*.

        Supports any real number (int, float, Decimal, etc.).
        Raises ``TypeError`` if *n* is not a real number.
        """
        try:
            result = n * n
        except Exception as exc:
            raise TypeError('square method expects a real number') from exc
        # Disallow complex results even if multiplication succeeded
        if isinstance(result, complex):
            raise TypeError('square method expects a real number')
        return result
