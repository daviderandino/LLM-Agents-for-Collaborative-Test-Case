import pytest
from data.input_code.t10 import *



def test_small_nnum_n_zero():
    assert small_nnum([1, 2, 3, 4, 5], 0) == []

