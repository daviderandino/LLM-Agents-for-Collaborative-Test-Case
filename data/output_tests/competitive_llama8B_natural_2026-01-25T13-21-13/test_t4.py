import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
    ([1, 2, 3], 5, [1, 2, 3]),  
    ([1, 2, 3], 0, []),
    ([1, 2, 3], 3, [3, 2, 1]),
    ([-1, -2, -3, -4, -5], 3, [-1, -2, -3]),
    ([1, 2, 2, 3, 4], 3, [4, 3, 2]),
    ([], 3, []),
    (None, 3, TypeError),
    ([1, 2, 3], 3.5, TypeError),
    ([1, 2, '3'], 3, TypeError)
])
def test_heap_queue_largest(nums, n, expected):
    if isinstance(expected, type):
        with pytest.raises(expected):
            heap_queue_largest(nums, n)
    else:
        assert heap_queue_largest(nums, n) == sorted(expected, reverse=True)