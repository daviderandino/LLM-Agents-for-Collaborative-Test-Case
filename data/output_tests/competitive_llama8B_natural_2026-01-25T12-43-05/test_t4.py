import pytest
from data.input_code.t4 import *

def test_heap_queue_largest_happy_path():
    nums = [10, 20, 30, 40, 50]
    n = 3
    expected = [50, 40, 30]
    assert heap_queue_largest(nums, n) == expected


def test_heap_queue_largest_negative_numbers():
    nums = [-10, -20, -30, -40, -50]
    n = 3
    expected = [-10, -20, -30]
    assert heap_queue_largest(nums, n) == expected

def test_heap_queue_largest_zero():
    nums = [0, 0, 0, 0, 0]
    n = 3
    expected = [0, 0, 0]
    assert heap_queue_largest(nums, n) == expected


def test_heap_queue_largest_n_equal_to_input_size():
    nums = [10, 20, 30]
    n = 3
    expected = [30, 20, 10]
    assert heap_queue_largest(nums, n) == expected

def test_heap_queue_largest_n_equal_to_1():
    nums = [10, 20, 30]
    n = 1
    expected = [30]
    assert heap_queue_largest(nums, n) == expected

def test_heap_queue_largest_duplicate_numbers():
    nums = [10, 20, 20, 30, 30]
    n = 3
    expected = [30, 30, 20]
    assert heap_queue_largest(nums, n) == expected

def test_heap_queue_largest_single_element_input():
    nums = [10]
    n = 1
    expected = [10]
    assert heap_queue_largest(nums, n) == expected

