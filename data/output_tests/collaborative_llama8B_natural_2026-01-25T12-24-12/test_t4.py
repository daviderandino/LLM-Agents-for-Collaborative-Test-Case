import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
    ([0, 0, 0, 0, 0], 3, [0, 0, 0]),
    ([-1, -2, -3, -4, -5], 3, [-1, -2, -3])
])
def test_heap_queue_largest_success(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected



def test_heap_queue_largest_n_equal_to_0():
    assert heap_queue_largest([1, 2, 3, 4, 5], 0) == []

