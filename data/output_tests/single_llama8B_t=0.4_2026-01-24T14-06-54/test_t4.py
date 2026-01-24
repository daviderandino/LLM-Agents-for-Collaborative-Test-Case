import pytest
from data.input_code.t4 import heap_queue_largest

def test_heap_queue_largest_valid_input():
    nums = [1, 2, 3, 4, 5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3]

def test_heap_queue_largest_zero_n():
    nums = [1, 2, 3, 4, 5]
    n = 0
    result = heap_queue_largest(nums, n)
    assert result == []




def test_heap_queue_largest_non_integer_n():
    nums = [1, 2, 3, 4, 5]
    n = 3.5
    with pytest.raises(TypeError):
        heap_queue_largest(nums, n)