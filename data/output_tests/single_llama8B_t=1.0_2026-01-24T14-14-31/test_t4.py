import pytest
from data.input_code.t4 import *


def test_default_success():
    nums = [1, 2, 3, 4, 5]
    n = 3
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3]








def test_edge_case_single_element_extracted():
    nums = [1, 1, 1, 1, 1]
    n = 1
    result = heap_queue_largest(nums, n)
    assert result == [1]


def test_edge_case_equal_number_of_elements_extracted():
    nums = [1, 2, 3, 4, 5]
    n = 5
    result = heap_queue_largest(nums, n)
    assert result == [5, 4, 3, 2, 1]






def test_none_input():
    nums = None
    n = 3
    with pytest.raises(TypeError):
        heap_queue_largest(nums, n)