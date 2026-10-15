import pytest
from simple_calculator import SimpleCalculator, CalculatorError


@pytest.fixture
def calc():
    return SimpleCalculator()


def test_division_by_zero_raises_calculator_error(calc):
    with pytest.raises(CalculatorError) as excinfo:
        calc.div(10, 0)
    assert "Division by zero is not allowed" in str(excinfo.value)


def test_normal_division(calc):
    assert calc.div(10, 2) == 5