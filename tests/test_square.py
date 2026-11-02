# -*- coding: utf-8 -*-

import pytest
from decimal import Decimal
from simple_calculator.main import SimpleCalculator


def test_square_positive_int():
    calc = SimpleCalculator()
    assert calc.square(5) == 25


def test_square_negative_int():
    calc = SimpleCalculator()
    assert calc.square(-3) == 9


def test_square_zero():
    calc = SimpleCalculator()
    assert calc.square(0) == 0


def test_square_float():
    calc = SimpleCalculator()
    assert calc.square(2.5) == 6.25


def test_square_decimal():
    calc = SimpleCalculator()
    assert calc.square(Decimal('1.2')) == Decimal('1.44')


def test_square_invalid_input_raises_type_error():
    calc = SimpleCalculator()
    with pytest.raises(TypeError):
        calc.square('not a number')
