import numbers

class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass

# Tolerance used to treat a denominator as “zero”.
EPSILON = 1e-12


class SimpleCalculator:
    def add(self, a, b):
        """Return the sum of a and b."""
        return a + b

    def sub(self, a, b):
        """Return the difference of a and b."""
        return a - b

    def mul(self, a, b):
        """Return the product of a and b."""
        return a * b

    def avg(self, numbers):
        """Return the average of a list of numbers."""
        if not numbers:
            raise CalculatorError("Cannot compute average of empty list")
        return sum(numbers) / len(numbers)

    def div(self, a: float, b: float) -> float:
        """Divide a by b.

        The method validates that both arguments are numeric and treats any
        denominator whose absolute value is smaller than ``EPSILON`` as zero.

        Returns:
            float: the quotient when b is not (effectively) zero.

        Raises:
            CalculatorError: if b is zero (or effectively zero) or if the
                inputs are not numeric.
        """
        # Type validation (accept any real number)
        if not isinstance(a, numbers.Real):
            raise CalculatorError(f"Invalid dividend {a!r}: must be a real number")
        if not isinstance(b, numbers.Real):
            raise CalculatorError(f"Invalid divisor {b!r}: must be a real number")

        # Zero-denominator handling with epsilon tolerance
        if abs(b) < EPSILON:
            raise CalculatorError(f"Division by zero is not allowed (denominator={b!r})")

        return a / b