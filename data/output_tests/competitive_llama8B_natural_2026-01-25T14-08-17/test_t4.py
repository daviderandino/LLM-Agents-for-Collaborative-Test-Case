import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([10, 20, 30, 40, 50], 3, [50, 40, 30]),
    ([10, 20, 0, 40, 50], 3, [50, 40, 20]),
    ([10, 10, 20, 40, 50], 3, [50, 40, 20]),
    ([-10, -20, -30, 40, 50], 3, [50, 40, -10]),  # Corrected expected value
])
def test_heap_queue_largest_success(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected


def test_heap_queue_largest_empty_list():
    assert heap_queue_largest([], 3) == []

def test_heap_queue_largest_n_zero():
    assert heap_queue_largest([10, 20, 30, 40, 50], 0) == []

