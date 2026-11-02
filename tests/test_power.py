# -*- coding: utf-8 -*-

import pytest

from simple_calculator.main import SimpleCalculator


def test_power_positive_exponent():
    calc = SimpleCalculator()
    assert calc.power(2, 3) == 8


def test_power_zero_exponent():
    calc = SimpleCalculator()
    assert calc.power(5, 0) == 1


def test_power_negative_exponent():
    calc = SimpleCalculator()
    assert pytest.approx(calc.power(2, -2)) == 0.25


def test_power_fractional_exponent():
    calc = SimpleCalculator()
    assert pytest.approx(calc.power(4, 0.5)) == 2.0


def test_power_invalid_base():
    calc = SimpleCalculator()
    with pytest.raises(ValueError):
        calc.power('a', 2)


def test_power_invalid_exponent():
    calc = SimpleCalculator()
    with pytest.raises(ValueError):
        calc.power(2, 'b')
