# -*- coding: utf-8 -*-

import operator
from functools import reduce


class SimpleCalculator:
    def add(self, *args):
        return sum(args)

    def sub(self, a, b):
        return a - b

    def mul(self, *args):
        # Return the product of all supplied arguments.
        # For an empty argument list the mathematical identity is 1.
        return reduce(operator.mul, args, 1)

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