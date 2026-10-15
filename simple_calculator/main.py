class SimpleCalculator:
    def add(self, *args):
        """Return the sum of all provided arguments."""
        return sum(args)

    def sub(self, a, b):
        """Return the result of subtracting b from a."""
        return a - b

    def mul(self, *args):
        """Return the product of all provided arguments.

        Raises:
            ValueError: If no arguments are provided.
        """
        if not args:
            raise ValueError("At least one argument required")
        result = 1
        for number in args:
            result *= number
        return result

    def avg(self, data, lt=None, ut=None):
        """Calculate the average of a list, optionally filtering values.

        Args:
            data (list of numbers): The list of numbers to average.
            lt (number, optional): Lower bound (inclusive). Values less than this are excluded.
            ut (number, optional): Upper bound (inclusive). Values greater than this are excluded.

        Returns:
            float: The average of the filtered list, or 0 if the list is empty after filtering.
        """
        filtered = [
            x for x in data
            if (lt is None or x >= lt) and (ut is None or x <= ut)
        ]
        if not filtered:
            return 0
        return sum(filtered) / len(filtered)

    def div(self, a, b):
        """Divide *a* by *b*.

        Returns:
            float: The quotient when ``b`` is not zero.

        Raises:
            ZeroDivisionError: If ``b`` is zero, with a clear error message.
        """
        if b == 0:
            raise ZeroDivisionError("Division by zero is not allowed")
        return a / b