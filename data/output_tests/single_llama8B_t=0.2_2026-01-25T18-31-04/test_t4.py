import pytest
from data.input_code.t4 import heap_queue_largest
import heapq as hq

def test_heap_queue_largest_success():
    nums = [1, 2, 3, 4, 5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3]






def test_heap_queue_largest_none():
    nums = None
    n = 3
    with pytest.raises(TypeError):
        heap_queue_largest(nums, n)

def test_heap_queue_largest_negative_number():
    nums = [-1, -2, -3, -4, -5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [-1, -2, -3]