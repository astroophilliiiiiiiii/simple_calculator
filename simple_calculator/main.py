# -*- coding: utf-8 -*-

import operator
from functools import reduce


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        """
        Multiply all given arguments.

        Raises:
            ValueError: If any argument is exactly zero.
        """
        # Raise only for numeric zero, not for other falsy values.
        if any(arg == 0 for arg in args):
            raise ValueError
        # ``reduce`` works for one or more arguments; for an empty call we
        # let Python raise the natural TypeError (mirroring the behaviour of
        # the built‑in ``math.prod`` in older Python versions).
        return reduce(operator.mul, args)

    def div(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return float("inf")

    def pow(self, a: float, b: float) -> float:
        """Return *a* raised to the power of *b*.

        Args:
            a: The base number.
            b: The exponent.

        Returns:
            The result of ``a ** b``.
        """
        return a ** b

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
