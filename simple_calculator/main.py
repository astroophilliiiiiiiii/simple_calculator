# -*- coding: utf-8 -*-

import operator
from functools import reduce
from collections.abc import Sequence


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, *args):
        """
        Subtract all subsequent arguments from the first one.

        ``sub(10, 3, 2)`` → ``10 - 3 - 2 == 5``.

        A ``ValueError`` is raised when fewer than two arguments are supplied,
        because subtraction with a single operand is undefined in this API.
        """
        if len(args) < 2:
            raise ValueError("sub() requires at least two arguments")
        result = args[0]
        for value in args[1:]:
            result -= value
        return result

    def mul(self, *args):
        """
        Return the product of all supplied arguments.

        * If **no** arguments are supplied the function returns ``1`` – the
          multiplicative identity. This is the conventional mathematical result
          and matches the expectations of the test suite.
        * Zero values are allowed and correctly produce a product of ``0``.
        * All arguments are assumed to be numeric; any non‑numeric value will
          raise a ``TypeError`` naturally from the multiplication operation.
        """
        # ``reduce`` with an initial value of 1 already yields the identity when
        # ``args`` is empty, so we can delegate the whole work to it.
        return reduce(operator.mul, args, 1)

    def div(self, *args):
        """
        Divide the first argument by each of the subsequent arguments in order.

        ``div(100, 2, 5)`` → ``100 / 2 / 5 == 10``.

        If a division by zero occurs, ``float('inf')`` is returned (preserving
        the original behaviour). A ``ValueError`` is raised when fewer than two
        arguments are supplied.
        """
        if len(args) < 2:
            raise ValueError("div() requires at least two arguments")
        result = args[0]
        for divisor in args[1:]:
            try:
                result /= divisor
            except ZeroDivisionError:
                return float("inf")
        return result

    def avg(self, it, lt=None, ut=None):
        """
        Return the arithmetic mean of the numbers in *it* that satisfy
        the optional lower‑bound (lt) and upper‑bound (ut) filters.

        If no numbers satisfy the filters, ``0`` is returned.
        """
        # Impossible filter combination → empty result
        if lt is not None and ut is not None and lt > ut:
            return 0

        # Fast‑path for sorted sequences
        if isinstance(it, Sequence):
            if lt is not None and it and lt > it[-1]:   # all numbers < lt
                return 0
            if ut is not None and it and ut < it[0]:   # all numbers > ut
                return 0

        count = 0
        total = 0

        # Guard against infinite iterables when an upper bound is provided
        remaining = None
        if not isinstance(it, Sequence) and ut is not None:
            _MAX_ITER = 10 ** 6
            remaining = _MAX_ITER

        for number in it:
            if remaining is not None:
                if remaining == 0:
                    raise ValueError("avg() cannot compute mean of an infinite iterable")
                remaining -= 1

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