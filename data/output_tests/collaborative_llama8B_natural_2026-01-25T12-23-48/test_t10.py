import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([10, 5, 8, 12, 3], 3, [3, 5, 8]),
    ([], 3, []),
    ([10, 5, 8], 5, [5, 8, 10]),
    ([10, 5, 8], 3, [5, 8, 10]),
    ([-10, -5, -8, 12, 3], 3, [-10, -8, -5]),
    ([10, 'a', 8, 12, 3], 3, TypeError),
    ([10, 5, 8, 12, 3], 2.5, TypeError),
    ([10, 5, 8, 12, 3, 7, 9, 1, 6, 4], 5, [1, 3, 4, 5, 6]),
    ([10, 10, 10, 10, 10], 3, [10, 10, 10])
])
def test_small_nnum(list1, n, expected):
    if isinstance(expected, type):
        with pytest.raises(expected):
            small_nnum(list1, n)
    else:
        assert small_nnum(list1, n) == expected