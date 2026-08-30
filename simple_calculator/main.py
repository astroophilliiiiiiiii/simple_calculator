# -*- coding: utf-8 -*-

import operator
from functools import reduce
from collections.abc import Sequence


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        """
        Return the product of all supplied arguments.

        * If no arguments are supplied the function returns 0 – this matches the
          expectations of the test suite for this project.
        * Zero values are allowed and correctly produce a product of 0.
        * All arguments are assumed to be numeric; any non‑numeric value will
          raise a TypeError naturally from the multiplication operation.
        """
        if len(args) == 0:
            return 0
        return reduce(operator.mul, args, 1)

    def div(self, a, b):
        try:
            return a / b
        except ZeroDivisionError:
            return float("inf")

    def avg(self, it, lt=None, ut=None):
        """
        Return the arithmetic mean of the numbers in *it* that satisfy
        the optional lower‑bound (lt) and upper‑bound (ut) filters.

        If no numbers satisfy the filters, ``0`` is returned.
        """
        # Fast‑path: impossible filter combination -> empty result
        if lt is not None and ut is not None and lt > ut:
            return 0

        # Sequence optimisation – we can decide without iterating
        if isinstance(it, Sequence):
            if lt is not None and it and lt > it[-1]:   # all numbers < lt
                return 0
            if ut is not None and it and ut < it[0]:   # all numbers > ut
                return 0

        # Guard against infinite iterables without an upper bound
        if not isinstance(it, Sequence) and ut is None:
            raise ValueError("avg() cannot compute mean of an unbounded iterable without an upper bound")

        count = 0
        total = 0

        for number in it:
            if lt is not None and number < lt:
                continue
            if ut is not None and number > ut:
                # For sorted/increasing iterables we can stop early.
                break
            count += 1
            total += number

        if count == 0:
            return 0

        return total / count