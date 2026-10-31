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

        Returns ``float('inf')`` if any divisor is zero, mirroring the original
        behaviour for a single division by zero.
        """
        if not args:
            raise ValueError("At least one operand is required for division")

        # Start with the first operand as the initial result
        result = args[0]
        for divisor in args[1:]:
            try:
                result = operator.truediv(result, divisor)
            except ZeroDivisionError:
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
