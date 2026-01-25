import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 3, 3], True),
    ([], False),
    ([5], False),
    ([1, 2, 3, 3, 2], True),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_empty():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_none():
    assert is_duplicate([1, 2, None]) == False


def test_is_duplicate_none_correct():
    assert is_duplicate([1, 2, None]) == False