import pytest
from data.input_code.t4 import heap_queue_largest

def test_heap_queue_largest_valid_input():
    nums = [1, 2, 3, 4, 5]
    n = 3
    expected_output = [5, 4, 3]
    assert heap_queue_largest(nums, n) == expected_output

def test_heap_queue_largest_valid_input_zero_n():
    nums = [1, 2, 3, 4, 5]
    n = 0
    assert heap_queue_largest(nums, n) == []

def test_heap_queue_largest_valid_input_n_greater_than_list_length():
    nums = [1, 2, 3, 4, 5]
    n = 10
    expected_output = [5, 4, 3, 2, 1]
    assert heap_queue_largest(nums, n) == expected_output

def test_heap_queue_largest_empty_list():
    nums = []
    n = 3
    assert heap_queue_largest(nums, n) == []

def test_heap_queue_largest_single_element_list():
    nums = [5]
    n = 3
    expected_output = [5]
    assert heap_queue_largest(nums, n) == expected_output

def test_heap_queue_largest_negative_input():
    nums = [1, 2, 3, -4, 5]
    n = 3
    expected_output = [5, 3, 2]
    assert heap_queue_largest(nums, n) == expected_output

def test_heap_queue_largest_non_integer_input():
    nums = [1.1, 2.2, 3.3, 4.4, 5.5]
    n = 3
    expected_output = [5.5, 4.4, 3.3]
    assert heap_queue_largest(nums, n) == expected_output


def test_heap_queue_largest_invalid_n_type():
    nums = [1, 2, 3, 4, 5]
    n = "hello"
    with pytest.raises(TypeError):
        heap_queue_largest(nums, n)