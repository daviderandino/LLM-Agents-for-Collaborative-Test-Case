import pytest
from data.input_code.t4 import heap_queue_largest

def test_heap_queue_largest_success():
    nums = [1, 2, 3, 4, 5]
    n = 3
    expected = [5, 4, 3]
    assert heap_queue_largest(nums, n) == expected






def test_heap_queue_largest_negative_numbers():
    nums = [-1, -2, -3, -4, -5]
    n = 3
    expected = [-1, -2, -3]
    assert heap_queue_largest(nums, n) == expected