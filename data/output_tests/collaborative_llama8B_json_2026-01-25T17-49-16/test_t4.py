import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
    ([], 3, []),
    ([10, 20, 30], 5, [30, 20, 10]),
    ([10, 20, 30], 0, []),
    ([10.5, 20.5, 30.5], 3, [30.5, 20.5, 10.5])
])
def test_heap_queue_largest_success(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected