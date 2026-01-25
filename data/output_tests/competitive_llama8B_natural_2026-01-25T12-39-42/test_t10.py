import pytest
from data.input_code.t10 import *


def test_small_nnum_empty_list():
    assert small_nnum([], 0) == []


def test_small_nnum_error_none_input():
    with pytest.raises(TypeError):
        small_nnum(None, 3)

def test_small_nnum_error_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([10, 20, 30], 3.5)

def test_small_nnum_error_non_integer_n2():
    with pytest.raises(TypeError):
        small_nnum([10, 20, 30], 'hello')

