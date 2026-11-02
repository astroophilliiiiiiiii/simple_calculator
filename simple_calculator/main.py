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

    def factorial(self, n):
        """
        Return the factorial of a non‑negative integer ``n``.

        * ``n`` must be an ``int`` – otherwise a ``TypeError`` is raised.
        * ``n`` must be >= 0 – otherwise a ``ValueError`` is raised.
        * ``0!`` and ``1!`` both return ``1``.
        """
        if not isinstance(n, int):
            raise TypeError('factorial() argument must be an integer')
        if n < 0:
            raise ValueError('factorial() not defined for negative numbers')

        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
