import pytest
from data.input_code.t4 import heap_queue_largest

# Test cases for max coverage with branch analysis
@pytest.mark.parametrize('nums,n,expected', [
    ([1, 2, 3, 4, 5], 2, [5, 4]),
    ([10, 3, 7, 1, 9], 3, [10, 9, 7]),
    ([-1, -5, 0], 2, [0, -1]),
    ([0, 0, 0], 2, [0, 0]),
])
def test_heap_queue_largest_valid_input(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected

# Test cases for boundary values


def test_heap_queue_largest_single_element():
    assert heap_queue_largest([10],1) == [10]

# Test cases for data types
def test_heap_queue_largest_empty_list():
    assert heap_queue_largest([], 2) == []

def test_heap_queue_largest_none_input():
    with pytest.raises(TypeError):
        heap_queue_largest(None, 2)

def test_heap_queue_largest_none_n():
    with pytest.raises(TypeError):
        heap_queue_largest([1, 2, 3], None)

# Test cases for edge cases
def test_heap_queue_largest_negative_nums():
    assert heap_queue_largest([-1, -2, -3], 2) == [-1, -2]

def test_heap_queue_largest_all_zeros():
    assert heap_queue_largest([0, 0, 0], 2) == [0, 0]