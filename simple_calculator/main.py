# -*- coding: utf-8 -*-

import operator
from functools import reduce
from typing import Iterable, Optional, Union


class SimpleCalculator:
    """A very small arithmetic helper supporting add, sub, mul, div and avg."""

    def add(self, *args: Union[int, float]) -> Union[int, float]:
        """Return the sum of all supplied numbers. No arguments → 0."""
        return sum(args)

    def sub(self, *args: Union[int, float]) -> Union[int, float]:
        """
        Subtract all subsequent arguments from the first one.

        Example:
            sub(10, 3, 2) -> 5
        """
        if not args:
            raise ValueError("sub() requires at least one operand")
        result = args[0]
        for value in args[1:]:
            result -= value
        return result

    def mul(self, *args: Union[int, float]) -> Union[int, float]:
        """
        Return the product of all supplied numbers.

        * Zero arguments → 0 (convenient default for a simple calculator).
        * Zero values are allowed – they correctly produce a product of 0.
        """
        if not args:
            return 0
        return reduce(operator.mul, args, 1)

    def div(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        """
        Return a / b.

        Division by zero is not silenced – the built‑in ZeroDivisionError
        is propagated.
        """
        return a / b

    def avg(
        self,
        it: Iterable[Union[int, float]],
        lt: Optional[Union[int, float]] = None,
        ut: Optional[Union[int, float]] = None,
    ) -> float:
        """
        Compute the average of numbers in *it* optionally bounded by
        lower (lt) and upper (ut) thresholds.

        Numbers outside the bounds are ignored. If no numbers remain,
        0.0 is returned.
        """
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
            return 0.0

        return total / count