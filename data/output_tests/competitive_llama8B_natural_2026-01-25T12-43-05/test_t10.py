import pytest
from data.input_code.t10 import *


def test_small_nnum_non_integer_n():
    with pytest.raises(TypeError):
        small_nnum([10, 20, 30, 40, 50], 3.5)


def test_small_nnum_none_input():
    with pytest.raises(TypeError):
        small_nnum([10, 20, 30, 40, 50], None)