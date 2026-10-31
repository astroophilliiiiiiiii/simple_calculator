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
        """Return the factorial of a non‑negative integer ``n``.

        * ``n`` must be an ``int`` and ``n >= 0``.
        * ``0!`` and ``1!`` both return ``1``.
        * Negative values raise ``ValueError``.
        * Non‑integer values raise ``TypeError``.
        """
        if not isinstance(n, int):
            raise TypeError("factorial() only accepts integer values")
        if n < 0:
            raise ValueError("factorial() not defined for negative numbers")
        if n in (0, 1):
            return 1
        # Compute product 1 * 2 * ... * n
        return reduce(operator.mul, range(1, n + 1))

    def square(self, n):
        """Return the square of *n*.

        Accepts ``int`` or ``float`` (including negative, zero and decimal
        numbers).  Any other type raises ``TypeError``.
        """
        if not isinstance(n, (int, float)):
            raise TypeError("square() only accepts numeric (int or float) values")
        return n * n
