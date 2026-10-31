# -*- coding: utf-8 -*-

import operator
from functools import reduce
from numbers import Real


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        """
        Multiply a sequence of numbers.

        * At least one argument is required.
        * All arguments must be real numbers (int or float).
        * Zero is treated as an illegal argument – raises ValueError.
        """
        # ---- validation -------------------------------------------------
        if not args:
            raise ValueError("mul() requires at least one argument")

        for arg in args:
            # reject None, strings, containers, etc.
            if not isinstance(arg, Real):
                raise ValueError(f"Non-numeric argument: {arg!r}")
            if arg == 0:
                raise ValueError("Zero is not allowed in multiplication")

        # ---- actual multiplication ---------------------------------------
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
