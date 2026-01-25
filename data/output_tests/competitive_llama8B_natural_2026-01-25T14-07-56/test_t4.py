import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([10, 20, 30, 40, 50], 3, [50, 40, 30]),
    ([-10, -20, -30, -40, -50], 3, [-10, -20, -30]),
    ([0, 0, 0, 0, 0], 3, [0, 0, 0]),
    ([10, 10, 20, 20, 30], 3, [30, 20, 20]),
])
def test_heap_queue_largest_success(nums, n, expected):
    assert heap_queue_largest(nums, n) == expected


def test_heap_queue_largest_n_equal_to_list_length():
    assert heap_queue_largest([10, 20, 30], 3) == [30, 20, 10]


def test_heap_queue_largest_none_input():
    with pytest.raises(TypeError):
        heap_queue_largest(None, 3)

