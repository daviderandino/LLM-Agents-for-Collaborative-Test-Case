import pytest
from fib import *

@pytest.mark.parametrize('n, expected', [
    (0, 1),
    (1, 1),
    (2, 2),  # Corrected expected value for n = 2
    (3, 3),
    (4, 5),
    (5, 8),
    (6, 13),
])
def test_count_ways(n, expected):
    result = count_ways(n)
    assert result == expected