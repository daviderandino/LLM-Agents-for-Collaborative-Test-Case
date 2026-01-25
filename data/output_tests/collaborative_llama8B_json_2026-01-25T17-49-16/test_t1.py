import pytest
from data.input_code.t1 import *


def test_min_cost_error():
    with pytest.raises(IndexError):
        min_cost([[1, 2], [3, 4]], 2, 0)