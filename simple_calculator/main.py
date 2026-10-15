# simple_calculator.py
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
        Multiply all arguments together.

        Raises:
            ValueError: If no arguments are supplied.
        """
        if not args:
            raise ValueError("At least one operand is required")
        # Using an initializer of 1 allows multiplication of any number of arguments,
        # including a single argument, and correctly handles zero values.
        return reduce(operator.mul, args, 1)

    def div(self, a, b):
        """
        Divide ``a`` by ``b``.

        Returns:
            float: The quotient when ``b`` is non‑zero.
            str:   An error message when ``b`` is zero.

        The method does not raise ``ZeroDivisionError``; instead it returns a
        clear, user‑friendly message so that callers (e.g. a UI) can display it
        without crashing.
        """
        if b == 0:
            # Graceful handling – return a message instead of raising.
            return "Error: Division by zero is not allowed"
        return a / b

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