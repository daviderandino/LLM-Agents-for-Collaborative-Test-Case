import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(IndexError):
        count_ways(-1)

# Fix the failing tests

@pytest.mark.parametrize('n', [-1, -2, -3, -4, -5])
def test_count_ways_error_fixed(n):
    with pytest.raises(IndexError):
        count_ways(n)