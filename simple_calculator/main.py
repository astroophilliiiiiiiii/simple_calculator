# -*- coding: utf-8 -*-

import operator
from functools import reduce
from collections.abc import Iterable


class SimpleCalculator:
    # --------------------------------------------------------------------- #
    # Private helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _ensure_number(value, name='value'):
        """Raise TypeError if *value* is not an int/float (or subclass)."""
        if not isinstance(value, (int, float)):
            raise TypeError(f'{name} must be a numeric type, got {type(value)!r}')

    @staticmethod
    def _ensure_iterable_of_numbers(it):
        """Validate *it* is an iterable (but not a string/bytes) of numbers.

        Returns a generator that yields the validated numbers one at a time.
        This works for any finite or infinite iterable.
        """
        # Guard against strings/bytes – they are iterable but not numeric
        if isinstance(it, (str, bytes)):
            raise TypeError('`it` must be an iterable of numbers, not a string/bytes')

        # Ensure the object is iterable at all
        if not isinstance(it, Iterable):
            raise TypeError('`it` must be an iterable of numbers')

        # Validate each element lazily and yield it
        for idx, item in enumerate(it):
            if not isinstance(item, (int, float)):
                raise TypeError(f'item {idx} in iterable is not numeric: {type(item)!r}')
            yield item

    # --------------------------------------------------------------------- #
    # Public API
    # --------------------------------------------------------------------- #
    def add(self, *args):
        for i, v in enumerate(args):
            self._ensure_number(v, f'arg {i}')
        # sum([]) correctly returns 0
        return sum(args)

    def sub(self, a, b):
        self._ensure_number(a, 'a')
        self._ensure_number(b, 'b')
        return a - b

    def mul(self, *args):
        """
        Multiply all supplied numbers.

        * If no arguments are given, the result is the multiplicative identity ``1``.
        * For a non‑empty argument list the numbers are multiplied together.
        """
        # Empty argument list → return 1 (the identity for multiplication)
        if not args:
            return 1
        for i, v in enumerate(args):
            self._ensure_number(v, f'arg {i}')
        # Reduce with identity 1 works for non‑empty sequences
        return reduce(operator.mul, args, 1)

    def div(self, a, b):
        self._ensure_number(a, 'a')
        self._ensure_number(b, 'b')
        if b == 0:
            # Consistent, explicit error message
            raise ZeroDivisionError('division by zero')
        return a / b

    def avg(self, it, lt=None, ut=None):
        """
        Compute the average of numbers in *it* optionally bounded by
        lower threshold *lt* and upper threshold *ut*.

        * Returns 0 when no numbers satisfy the constraints.
        * Raises TypeError for non‑iterable *it* or non‑numeric elements.
        """
        # Validate thresholds first
        if lt is not None:
            self._ensure_number(lt, 'lt')
        if ut is not None:
            self._ensure_number(ut, 'ut')

        # Ensure we have a proper iterable of numbers
        iterator = self._ensure_iterable_of_numbers(it)

        count = 0
        total = 0

        for number in iterator:
            # number is already guaranteed numeric by the helper
            if lt is not None and number < lt:
                continue
            if ut is not None and number > ut:
                continue
            count += 1
            total += number

        if count == 0:
            return 0

        return total / count