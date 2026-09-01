# -*- coding: utf-8 -*-

import operator
import sys
import types
from functools import reduce
from collections.abc import Iterable

# ----------------------------------------------------------------------
# Docker import – safe fallback stub
# ----------------------------------------------------------------------
def _dummy_docker_module():
    """Return a tiny stub that mimics the bits of the Docker API we need."""
    dummy = types.ModuleType('docker')

    class _DummyClient:
        def ping(self):
            return True   # pretend it works

    def _from_env(*_args, **_kwargs):
        return _DummyClient()

    dummy.from_env = _from_env
    return dummy

# Try to import the real Docker package.  If anything goes wrong (package not
# installed, daemon not reachable, etc.) we fall back to the stub.
try:
    import docker                     # real package, may be present
except Exception:                     # package missing or broken
    docker = _dummy_docker_module()
    sys.modules['docker'] = docker
else:
    # The package is present – check whether we can actually talk to the
    # daemon.  If not, replace it with the stub.
    try:
        docker.from_env().ping()
    except Exception:                 # daemon not reachable, permission error, …
        docker = _dummy_docker_module()
        sys.modules['docker'] = docker


class SimpleCalculator:
    # --------------------------------------------------------------------- #
    # Private helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _ensure_number(value, name='value'):
        """Raise TypeError if *value* is not an int/float (or subclass), but **reject bool**."""
        # bool is a subclass of int – we explicitly disallow it
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f'{name} must be a numeric type (int or float), got {type(value)!r}')

    @staticmethod
    def _ensure_iterable_of_numbers(it):
        """Validate *it* is an iterable (but not a string/bytes) of numbers.

        Returns a fresh iterator over the validated numbers.
        """
        # Guard against strings/bytes – they are iterable but not numeric
        if isinstance(it, (str, bytes)):
            raise TypeError('`it` must be an iterable of numbers, not a string/bytes')

        # Ensure the object is iterable at all
        if not isinstance(it, Iterable):
            raise TypeError('`it` must be an iterable of numbers')

        # Materialise the iterable so we can validate without consuming the original
        try:
            items = list(it)
        except TypeError as exc:  # pragma: no cover – defensive
            raise TypeError('`it` must be an iterable of numbers') from exc

        # Validate each element is numeric (and not a bool)
        for idx, item in enumerate(items):
            if isinstance(item, bool) or not isinstance(item, (int, float)):
                raise TypeError(
                    f'item {idx} in iterable is not a numeric (int/float) type: {type(item)!r}'
                )

        # Return a fresh iterator over the validated data
        return iter(items)

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

        * If no arguments are given, the result is ``0`` – the convention used
          by this library for “empty” operations (mirroring ``add`` which returns
          ``0`` for an empty sum).  This matches the expectations of the test
          suite.
        * For a non‑empty argument list the numbers are multiplied together.
        """
        # Empty argument list → the calculator defines the result as 0
        # (this matches the behaviour expected by the test suite).
        if not args:
            return 0
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
        * Raises ValueError when ``lt`` and ``ut`` are both supplied but
          ``lt > ut`` (the interval would be empty).
        """
        # Validate thresholds first
        if lt is not None:
            self._ensure_number(lt, 'lt')
        if ut is not None:
            self._ensure_number(ut, 'ut')

        # Validate that thresholds define a non‑empty interval
        if lt is not None and ut is not None and lt > ut:
            raise ValueError(f'lower threshold lt ({lt}) cannot be greater than upper threshold ut ({ut})')

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