import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([10, 20, 30, 40, 50], 3, [50, 40, 30]),
    ([0, 0, 0, 0, 0], 3, [0, 0, 0]),
    ([-10, -20, -30, -40, -50], 3, [-10, -20, -30]),
    ([10, 10, 10, 10, 10], 3, [10, 10, 10]),
])
def test_heap_queue_largest_success(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected


def test_heap_queue_largest_n_equals_list_length():
    assert heap_queue_largest([10, 20, 30], 3) == [30, 20, 10]

def test_heap_queue_largest_empty_list():
    assert heap_queue_largest([], 3) == []

def test_heap_queue_largest_n_equals_zero():
    assert heap_queue_largest([10, 20, 30], 0) == []

def test_heap_queue_largest_invalid_data_type():
    with pytest.raises(TypeError):
        heap_queue_largest([10, 20, 'c', 30, 40], 3)  # Changed to a mix of int and str