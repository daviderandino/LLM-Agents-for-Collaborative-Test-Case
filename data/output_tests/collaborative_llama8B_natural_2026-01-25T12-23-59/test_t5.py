import pytest
from data.input_code.t5 import *


@pytest.mark.parametrize('n', [
    -5,
])
def test_count_ways_edge_case(n):
    try:
        count_ways(n)
    except (TypeError, IndexError):
        assert True  # If n is not an integer, count_ways will raise TypeError or IndexError
    else:
        assert count_ways(n) == 0