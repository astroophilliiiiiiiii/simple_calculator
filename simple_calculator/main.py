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

    def div(self, *args):
        """Divide a sequence of numbers left‑to‑right.

        Returns ``float('inf')`` if **any** divisor is zero (including ``0``,
        ``0.0``, ``-0.0``, ``Decimal(0)`` etc.).
        Raises ``ValueError`` if fewer than two arguments are supplied.
        Otherwise returns the result of the left‑to‑right division as a ``float``.
        """
        if len(args) < 2:
            raise ValueError("div() requires at least two arguments")

        # Start with the first operand, cast to float for consistent return type.
        result = float(args[0])

        for divisor in args[1:]:
            # Any zero‑like divisor should cause an immediate ``inf`` result.
            if divisor == 0:
                return float("inf")
            result = result / divisor

        return result

    def avg(self, it, lt=None, ut=None):
        # Initialise counters.
        # ``total`` must start at 0 so that we can add numbers safely.
        # Using ``0.0`` guarantees a float result even when the iterable
        # contains only integers, matching the behaviour of the existing
        # tests that expect a float division.
        count = 0
        total = 0.0
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
