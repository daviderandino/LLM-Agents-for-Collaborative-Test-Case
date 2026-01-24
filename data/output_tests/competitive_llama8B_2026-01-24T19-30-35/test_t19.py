import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 4, 5], True),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected


def test_is_duplicate_none():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_empty_set():
    # The source code does not raise TypeError for empty set inputs, but it does not handle them either
    # It will return False for empty set inputs because len(nums_set) will be 0 and len(arraynums) will also be 0
    # So, we can check the result
    result = is_duplicate(set())
    assert result is False

def test_is_duplicate_none_set():
    # The source code does not raise TypeError for None set inputs, but it does not handle them either
    # It will raise TypeError for None inputs because set() cannot be created with None
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_single_element():
    assert not is_duplicate([1])

def test_is_duplicate_single_element_set():
    assert not is_duplicate(set([1]))