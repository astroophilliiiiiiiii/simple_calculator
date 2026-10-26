import numbers
import math
from typing import Iterable, Optional, List

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass


class SimpleCalculator:
    # Tolerance used to decide whether a floating‑point divisor is “zero”.
    # 1e‑12 works well for typical double‑precision calculations; adjust if
    # your domain needs a different precision.
    _ZERO_TOL = 1e-12

    # -----------------------------------------------------------------
    #  ADD / SUB / MUL
    # -----------------------------------------------------------------
    def add(self, *values: numbers.Real) -> numbers.Real:
        """Return the sum of *all* supplied numbers.

        Raises:
            CalculatorError: if no operands are provided or any operand
                is not a real number.
        """
        if not values:
            raise CalculatorError("add() requires at least one operand")
        total = 0
        for v in values:
            if not isinstance(v, numbers.Real):
                raise CalculatorError(f"Invalid operand {v!r}: must be a real number")
            total += v
        return total

    def sub(self, a: numbers.Real, b: numbers.Real) -> numbers.Real:
        """Return the difference a - b."""
        return a - b

    def mul(self, *values: numbers.Real) -> numbers.Real:
        """Return the product of *all* supplied numbers.

        Raises:
            CalculatorError: if no operands are provided or any operand
                is not a real number.
            ValueError: if any operand is zero.
        """
        if not values:
            raise CalculatorError("mul() requires at least one operand")
        product = 1
        for v in values:
            if not isinstance(v, numbers.Real):
                raise CalculatorError(f"Invalid operand {v!r}: must be a real number")
            if v == 0:
                raise ValueError("Multiplication by zero is not allowed")
            product *= v
        return product

    # -----------------------------------------------------------------
    #  DIVISION
    # -----------------------------------------------------------------
    def div(self, a: float, b: float) -> float:
        """Divide *a* by *b*.

        Returns ``math.inf`` when *b* is zero (or effectively zero) instead
        of raising an exception – this matches the behaviour required by the
        tests.
        """
        # Type validation (accept any real number)
        if not isinstance(a, numbers.Real):
            raise CalculatorError(f"Invalid dividend {a!r}: must be a real number")
        if not isinstance(b, numbers.Real):
            raise CalculatorError(f"Invalid divisor {b!r}: must be a real number")

        # Guard against NaN or infinite operands
        if math.isnan(a) or math.isinf(a):
            raise CalculatorError(f"Invalid dividend {a!r}: must be a finite number")
        if math.isnan(b) or math.isinf(b):
            raise CalculatorError(f"Invalid divisor {b!r}: must be a finite number")

        # Zero‑denominator handling – pure absolute‑tolerance check
        # The divisor is considered zero when |b| <= _ZERO_TOL
        if abs(b) <= self._ZERO_TOL:
            return math.inf

        return a / b

    # -----------------------------------------------------------------
    #  AVERAGE WITH OPTIONAL OUTLIER FILTERING
    # -----------------------------------------------------------------
    def avg(
        self,
        values: Iterable[numbers.Real],
        *,
        lt: Optional[float] = None,
        ut: Optional[float] = None,
    ) -> float:
        """
        Compute the arithmetic mean of *values*.

        Parameters
        ----------
        values : iterable of numbers
            The data set to average.
        lt : float, optional
            Lower threshold – values **strictly less** than ``lt`` are discarded.
            If ``None`` no lower filtering is performed.
        ut : float, optional
            Upper threshold – values **strictly greater** than ``ut`` are discarded.
            If ``None`` no upper filtering is performed.

        Returns
        -------
        float
            The average of the filtered collection, or ``0.0`` when the
            collection is empty (either originally or after applying the
            thresholds).
        """
        # Materialise the iterable so we can filter and compute length.
        data: List[float] = list(values)

        # Apply lower threshold if provided (inclusive).
        if lt is not None:
            data = [x for x in data if x >= lt]

        # Apply upper threshold if provided (inclusive).
        if ut is not None:
            data = [x for x in data if x <= ut]

        if not data:
            return 0.0

        return sum(data) / len(data)

    # -----------------------------------------------------------------
    #  LEGACY AVERAGE (kept for backward compatibility)
    # -----------------------------------------------------------------
    def avg_simple(self, values: Iterable[numbers.Real]) -> float:
        """Legacy helper – same behaviour as the original implementation."""
        vals = list(values)
        if not vals:
            raise CalculatorError("Cannot compute average of empty list")
        return sum(vals) / len(vals)