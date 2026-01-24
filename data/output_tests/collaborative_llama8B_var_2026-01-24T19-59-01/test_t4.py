import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
    ([1, 2, 3, 4, 5], 6, [5, 4, 3, 2, 1]),
    ([1, 2, 3, 4, 5], 0, []),
    ([], 3, []),
    ([1], 3, [1])
])
def test_heap_queue_largest(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected