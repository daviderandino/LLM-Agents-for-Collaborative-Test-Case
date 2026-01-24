import pytest
from data.input_code.t8 import square_nums

@pytest.mark.parametrize("nums, expected", [
    ([1, 2, 3], [1, 4, 9]),
    ([-1, 0, 1], [1, 0, 1]),
    ([], []),
    (None, []),
    ([], []),
])
def test_square_nums_list_nums(num, expected):
    assert square_nums(num) == expected

from data.input_code.t8 import square_nums

@pytest.mark.parametrize("nums, expected", [
    ("1 2 3", [1, 4, 9]),
    ("-1 0 1", [1, 0, 1]),
    ("", []),
    (None, []),
])
def test_square_nums_tuple_nums(num, expected):
    assert square_nums(num) == expected

from data.input_code.t8 import square_nums

def test_square_nums_empty():
    assert square_nums(None) == []