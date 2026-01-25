import pytest
from data.input_code.t4 import heap_queue_largest
import heapq as hq

def test_heap_queue_largest_success():
    nums = [1, 2, 3, 4, 5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3]


def test_heap_queue_largest_zero_n():
    nums = [1, 2, 3, 4, 5]
    n = 0
    result = heap_queue_largest(nums, n)
    assert result == []


def test_heap_queue_largest_large_n():
    nums = [1, 2, 3, 4, 5]
    n = 10
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3, 2, 1]


def test_heap_queue_largest_none_input():
    nums = None
    n = 3
    with pytest.raises(TypeError):
        heap_queue_largest(nums, n)