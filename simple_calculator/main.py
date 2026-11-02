# -*- coding: utf-8 -*-

import operator
from functools import reduce


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
            return float("inf")

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

    def power(self, base, exponent):
        """Return base raised to the exponent.

        Supports positive, negative, zero, and fractional exponents.
        Raises ValueError if either argument is not a numeric type.
        """
        if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
            raise ValueError('Both base and exponent must be numeric')
        return base ** exponent
