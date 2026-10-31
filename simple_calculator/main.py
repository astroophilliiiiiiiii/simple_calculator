# -*- coding: utf-8 -*-

import operator
from functools import reduce
from numbers import Number
from collections.abc import Iterable


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
        """Calculate the arithmetic mean of *it* with optional lower and upper
        thresholds.

        Parameters
        ----------
        it : iterable of numbers
            The collection (or generator) of numeric values to average.
        lt : number, optional
            Lower threshold (inclusive). Values strictly less than ``lt`` are
            ignored.
        ut : number, optional
            Upper threshold (inclusive). Values strictly greater than ``ut``
            are ignored.

        Returns
        -------
        float
            The average of the remaining numbers, or ``0`` if no numbers remain
            after filtering.

        Raises
        ------
        ValueError
            If *it* is not iterable, if any element of *it* is not numeric, or if
            ``lt``/``ut`` are provided but are not numeric.
        """
        # ---- validation -------------------------------------------------
        if not isinstance(it, Iterable):
            raise ValueError("`it` must be an iterable of numbers")

        if lt is not None and not isinstance(lt, Number):
            raise ValueError("`lt` must be a numeric value")
        if ut is not None and not isinstance(ut, Number):
            raise ValueError("`ut` must be a numeric value")

        count = 0
        total = 0.0

        for number in it:
            if not isinstance(number, Number):
                raise ValueError("All items in `it` must be numeric")
            if lt is not None and number < lt:
                continue
            if ut is not None and number > ut:
                continue
            count += 1
            total += float(number)

        if count == 0:
            return 0

        return total / count

    def factorial(self, n):
        """Return the factorial of a non‑negative integer *n*.

        Parameters
        ----------
        n : int
            The number whose factorial is required. Must be ``n >= 0``.

        Returns
        -------
        int
            ``n!`` – the product of all integers from 1 to *n* (``0!`` is 1).

        Raises
        ------
        ValueError
            If *n* is not an integer or is negative.
        """
        # Validation
        if not isinstance(n, int):
            raise ValueError("factorial() only accepts integer values")
        if n < 0:
            raise ValueError("factorial() not defined for negative integers")

        # Base cases
        if n == 0 or n == 1:
            return 1

        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
