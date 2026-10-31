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

        Returns ``float('inf')`` if any divisor is zero.
        Raises ``ValueError`` if fewer than two arguments are supplied.
        """
        if len(args) < 2:
            raise ValueError("div() requires at least two arguments")
        result = args[0]
        for divisor in args[1:]:
            try:
                result = result / divisor
            except ZeroDivisionError:
                return float("inf")
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
