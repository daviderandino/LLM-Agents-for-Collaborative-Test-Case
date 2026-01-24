import pytest
from data.input_code.t4 import *


def test_heap_queue_largest_empty_list():
    assert heap_queue_largest([], 3) == []

def test_heap_queue_largest_none_input():
    with pytest.raises(TypeError):
        heap_queue_largest(None, 3)

def test_heap_queue_largest_non_numeric_input():
    with pytest.raises(TypeError):
        heap_queue_largest([10, 'a', 30, 40, 50], 3)

