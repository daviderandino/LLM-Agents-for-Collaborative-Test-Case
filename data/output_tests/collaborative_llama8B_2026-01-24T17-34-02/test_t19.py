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



def test_is_duplicate_none_set():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_is_duplicate_single_element():
    assert is_duplicate([1]) == False

def test_is_duplicate_single_element_set():
    assert is_duplicate(set([1])) == False


def test_is_duplicate_none_list():
    with pytest.raises(TypeError):
        is_duplicate(None)



def test_is_duplicate_none_set_list():
    with pytest.raises(TypeError):
        is_duplicate(None)

