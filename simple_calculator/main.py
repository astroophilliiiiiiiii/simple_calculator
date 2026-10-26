class CalculatorError(Exception):
    """Custom exception for calculator errors."""
    pass


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

        Returns:
            float: the quotient when b != 0

        Raises:
            CalculatorError: if b == 0
        """
        if b == 0:
            raise CalculatorError("Division by zero is not allowed")
        return a / b