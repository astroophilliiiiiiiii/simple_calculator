# -*- coding: utf-8 -*-

import operator
import sys
import types
import numbers
from functools import reduce
from collections.abc import Iterable

# ----------------------------------------------------------------------
# Optional NumPy support – we only need it to recognise ndarray as a
# collection of numbers.  If NumPy is not available the code must keep
# working, so we import it lazily and fall back to ``None``.
# ----------------------------------------------------------------------
try:                     # pragma: no cover – exercised only when NumPy is present
    import numpy as np
except Exception:       # pragma: no cover – NumPy not installed or broken
    np = None

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

# Try to import the real Docker package.  If *anything* goes wrong we replace it
# with the stub – we never let an exception escape the import.
try:
    import docker  # real package, may be present
    # Verify that we can actually talk to the daemon; any problem falls back.
    docker.from_env().ping()
except Exception:               # package missing, import error, ping failure, …
    docker = _dummy_docker_module()
    sys.modules['docker'] = docker


class SimpleCalculator:
    # --------------------------------------------------------------------- #
    # Private helpers
    # --------------------------------------------------------------------- #
    @staticmethod
    def _ensure_number(value, name='value'):
        """Raise TypeError if *value* is not a numeric type (subclass of numbers.Number),
        but **reject bool**."""
        # bool is a subclass of int – we explicitly disallow it
        if isinstance(value, bool) or not isinstance(value, numbers.Number):
            raise TypeError(f'{name} must be a numeric type (int, float, Decimal, Fraction, …), got {type(value)!r}')

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
            if isinstance(item, bool) or not isinstance(item, numbers.Number):
                raise TypeError(
                    f'item {idx} in iterable is not a numeric (int/float/Decimal/…) type: {type(item)!r}'
                )

        # Return a fresh iterator over the validated data
        return iter(items)

    @staticmethod
    def _is_collection_of_numbers(obj):
        """
        Return True if *obj* looks like a container of numbers.

        * It must be iterable (but not a string/bytes).
        * It must **not** be an instance of numbers.Number – because a
          numeric scalar can be iterable (e.g. numpy.ndarray) and we want
          to treat it as a scalar.
        """
        # Strings/bytes are iterable but should never be treated as a numeric
        # collection.
        if isinstance(obj, (str, bytes)):
            return False

        # NumPy nd‑arrays are *also* instances of ``numbers.Number`` (because they
        # implement the numeric protocol) but they are containers that we want
        # to iterate over.  If NumPy is available and ``obj`` is an ``ndarray`` we
        # explicitly treat it as a collection.
        if np is not None and isinstance(obj, np.ndarray):
            return True

        # Plain numeric scalars (int, float, Decimal, Fraction, …) must be
        # excluded – they are not collections even if they happen to be
        # iterable (e.g. ``numpy.float64`` can be iterable in some edge cases).
        if isinstance(obj, numbers.Number):
            return False

        # Anything else that is iterable (list, tuple, set, generator, …) is a
        # collection of numbers.
        return isinstance(obj, Iterable)

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
        Multiply numbers.

        * If called with a single *collection* (list, tuple, set, generator,
          …) the elements of the collection are multiplied.
        * If the collection is empty the result is **0** (calculator‑style
          semantics – nothing to multiply yields zero).
        * If called with a single scalar numeric argument, that scalar is
          returned unchanged.
        * If called with several numeric arguments, they are multiplied.
        * An empty argument list yields ``1`` (the multiplicative identity).
        """
        # No arguments → multiplicative identity
        if not args:
            return 1

        # Single argument – decide whether it is a collection or a scalar
        if len(args) == 1 and self._is_collection_of_numbers(args[0]):
            numbers_iter = self._ensure_iterable_of_numbers(args[0])
            numbers = list(numbers_iter)
            if not numbers:               # empty collection
                return 0
            return reduce(operator.mul, numbers, 1)

        # At this point we have either a single scalar or several scalars
        for i, v in enumerate(args):
            self._ensure_number(v, f'arg {i}')
        return reduce(operator.mul, args, 1)

    def div(self, a, b):
        """Divide *a* by *b*.

        Validates numeric inputs; Python's division operator raises the
        appropriate ZeroDivisionError for a zero divisor.
        """
        self._ensure_number(a, 'a')
        self._ensure_number(b, 'b')
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