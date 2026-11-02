#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from simple_calculator.main import SimpleCalculator


@pytest.fixture
def calc():
    return SimpleCalculator()


def test_factorial_of_zero(calc):
    assert calc.factorial(0) == 1


def test_factorial_of_one(calc):
    assert calc.factorial(1) == 1


def test_factorial_small_number(calc):
    assert calc.factorial(5) == 120


def test_factorial_larger_number(calc):
    # 10! = 3_628_800
    assert calc.factorial(10) == 3628800


def test_factorial_negative_raises(calc):
    with pytest.raises(ValueError):
        calc.factorial(-3)


@pytest.mark.parametrize('bad_input', [3.5, '5', None, [5], {5}])
def test_factorial_non_int_raises(calc, bad_input):
    with pytest.raises(TypeError):
        calc.factorial(bad_input)
