# -*- coding: utf-8 -*-

import operator
from functools import reduce
from numbers import Real
from typing import Iterable, Optional


class SimpleCalculator:
    """A very small calculator with explicit input validation."""

    @staticmethod
    def _validate_number(value, name: str = "value"):
        """
        Ensure *value* is a real number (int or float) and not ``None``.
        Raises:
            ValueError: if the value is ``None`` or not a number.
        """
        if value is None or not isinstance(value, Real):
            raise ValueError(f"{name} must be a real number, got {value!r}")

    def add(self, *args):
        """Return the sum of all arguments."""
        # ``sum`` already raises a sensible TypeError for non‑numeric args,
        # which is acceptable for the public contract.
        return sum(args)

    def sub(self, a, b):
        """Return the subtraction of *b* from *a*."""
        return a - b

    def mul(self, *args):
        """
        Multiply all arguments.

        * Zero is considered an invalid operand and raises ``ValueError``.
        * Non‑numeric arguments also raise ``ValueError`` (instead of a raw
          ``TypeError`` from ``operator.mul``).
        """
        if not args:
            raise ValueError("At least one argument is required")

        for i, arg in enumerate(args):
            self._validate_number(arg, f"arg[{i}]")
            if arg == 0:
                # Preserve the original contract that multiplying by zero is illegal.
                raise ValueError("Multiplication by zero is not allowed")

        # All arguments are valid numbers and non‑zero.
        return reduce(operator.mul, args)

    def div(self, a, b):
        """Return the division of *a* by *b*; ``inf`` on division by zero."""
        try:
            return a / b
        except ZeroDivisionError:
            return float("inf")

    def avg(self, it: Iterable, lt: Optional[Real] = None, ut: Optional[Real] = None):
        """
        Compute the average of *it* optionally filtering out values
        lower than ``lt`` or higher than ``ut`` (both thresholds are inclusive).

        Validation:
        * ``it`` must be an iterable (not ``None``).
        * Every element must be a real number.
        * ``lt`` and ``ut`` (if supplied) must be real numbers.
        """
        if it is None:
            raise ValueError("The iterable to average cannot be None")

        # Validate optional thresholds
        if lt is not None:
            self._validate_number(lt, "lt")
        if ut is not None:
            self._validate_number(ut, "ut")

        count = 0
        total = 0

        for idx, number in enumerate(it):
            self._validate_number(number, f"it[{idx}]")
            if lt is not None and number < lt:
                continue
            if ut is not None and number > ut:
                continue
            count += 1
            total += number

        if count == 0:
            return 0

        return total / count
