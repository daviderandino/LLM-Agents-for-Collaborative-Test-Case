import pytest
from data.input_code.t4 import heap_queue_largest

def test_heap_queue_largest_success():
    nums = [15, 22, 13, 11, 20]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [22, 20, 15]

def test_heap_queue_largest_edge_case_zero_n():
    nums = [15, 22, 13, 11, 20]
    n = 0
    result = heap_queue_largest(nums, n)
    assert result == []

def test_heap_queue_largest_edge_case_n_equal_length():
    nums = [15, 22, 13, 11, 20]
    n = len(nums)
    result = heap_queue_largest(nums, n)
    assert result == sorted(nums, reverse=True)



