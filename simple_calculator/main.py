# -*- coding: utf-8 -*-

import operator
from functools import reduce


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        # Return 0 for empty input to be consistent with add([]) → 0.
        if len(args) == 0:
            return 0
        # No special falsy-value check – zero is allowed.
        return reduce(operator.mul, args)

    def div(self, a, b):
        # Let Python raise ZeroDivisionError for b == 0.
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