import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 2, 4], True),
    ([1, 2, 3, 4, 5], False),
    ([], False),
    ([1], False),
    ([1, 1], True),
    ([-1, -2, -3, -2], True),
    ([1.0, 2.0, 3.0, 2.0], True),
    ([1, 'a', 3, 'a'], True),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_error():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_empty_list():
    assert is_duplicate([]) == False  # This test is actually correct, the function returns False for an empty list

def test_is_duplicate_single_element():
    assert is_duplicate([1]) == False  # This test is actually correct, the function returns False for a list with a single element

def test_is_duplicate_duplicate_elements():
    assert is_duplicate([1, 1]) == True  # This test is actually correct, the function returns True for a list with duplicate elements

