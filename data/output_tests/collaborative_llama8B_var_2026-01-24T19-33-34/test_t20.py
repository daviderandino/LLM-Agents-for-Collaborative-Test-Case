import pytest
from data.input_code.t20 import *

@pytest.mark.parametrize('m, n, expected', [
    (3, 2, [2, 4, 6]),
    (0, 2, []),
    (3, 0, []),
    (-3, 2, []),
    (3, -2, [])
])
def test_multiples_of_num(m, n, expected):
    if n == 0:
        with pytest.raises(ValueError):
            multiples_of_num(m, n)
    else:
        assert multiples_of_num(m, n) == list(range(n, (m+1)*n, n))