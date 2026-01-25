import pytest
from data.input_code.t4 import heap_queue_largest

def test_heap_queue_largest_success():
    nums = [1, 2, 3, 4, 5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3]





def test_heap_queue_largest_negative_num():
    nums = [-1, -2, -3]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [-1, -2, -3]

def test_heap_queue_largest_zero_num():
    nums = [0, 0, 0]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [0, 0, 0]

def test_heap_queue_largest_single_element():
    nums = [5]
    n = 1
    result = heap_queue_largest(nums, n)
    assert result == [5]