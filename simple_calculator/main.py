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
        """
        Divide a sequence of numbers left‑to‑right.

        * If *no* arguments are supplied a ``ValueError`` is raised – the
          original API always required at least two numbers, so this mirrors
          that expectation.
        * If any divisor (any argument after the first) is zero the method
          returns ``float('inf')`` instead of raising ``ZeroDivisionError``.
        * Works with negative numbers, decimals and a zero numerator.
        * When a single argument is supplied the method simply returns it,
          matching the intuitive “divide by nothing” behaviour.
        """
        if not args:
            raise ValueError("At least one operand is required for division")

        # Start with the first value; if there is only one value we just return it.
        result = args[0]

        for divisor in args[1:]:
            try:
                result = result / divisor
            except ZeroDivisionError:
                # Any zero divisor results in an infinite value.
                return float("inf")

        return result

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
