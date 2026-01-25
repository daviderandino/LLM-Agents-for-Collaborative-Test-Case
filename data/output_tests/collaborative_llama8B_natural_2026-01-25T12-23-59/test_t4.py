import pytest
from data.input_code.t4 import *


def test_heap_queue_largest_negative_numbers():
    assert heap_queue_largest([-1, -2, 3, 4, 5], 3) == [5, 4, 3]

def test_heap_queue_largest_mixed_input():
    assert heap_queue_largest([-1, -2, 3, 4, 5], 3) == [5, 4, 3]

def test_heap_queue_largest_zero_input():
    assert heap_queue_largest([1, 2, 3], 0) == []

def test_heap_queue_largest_larger_n():
    assert heap_queue_largest([1, 2, 3], 5) == [3, 2, 1]