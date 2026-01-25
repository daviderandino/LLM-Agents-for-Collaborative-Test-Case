import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([10, 20, 30, 40, 50], 3, [10, 20, 30]),
])
def test_small_nnum_happy_path(list1, n, expected):
    assert small_nnum(list1, n) == expected


def test_small_nnum_n_greater_than_list_length():
    assert small_nnum([10, 20, 30, 40], 5) == [10, 20, 30, 40]

def test_small_nnum_n_equal_to_list_length():
    assert small_nnum([10, 20, 30, 40, 50], 5) == [10, 20, 30, 40, 50]



def test_small_nnum_large_list():
    assert small_nnum([i for i in range(1000000)], 3) == [0, 1, 2]


# Fix the assertions in the test code so they match the Source Code logic and PASS


