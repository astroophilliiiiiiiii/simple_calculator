# -*- coding: utf-8 -*-

import operator
import math
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

    def pow(self, a, b):
        """Return a raised to the power of b."""
        return a ** b

    def sqrt(self, n):
        """Return the square root of ``n``.

        * For ``n >= 0`` the mathematical square root is returned.
        * For ``n < 0`` the function returns ``None`` instead of raising
          an exception, providing graceful handling of invalid input.
        """
        if n < 0:
            return None
        return math.sqrt(n)
