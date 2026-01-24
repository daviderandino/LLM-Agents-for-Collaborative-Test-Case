import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 2, 3, 4], True),
    ([1, 2, 3, 4], False),
    ([], False),
    ([5], False),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_empty():
    with pytest.raises(TypeError):
        is_duplicate(None)

def test_is_duplicate_non_list():
    with pytest.raises(TypeError):
        is_duplicate('1234')

def test_is_duplicate_non_hashable():
    with pytest.raises(TypeError):
        is_duplicate([[1, 2], [3, 4]])

def test_is_duplicate_large():
    assert is_duplicate([1]*10000)

def test_is_duplicate_non_list_type():
    with pytest.raises(TypeError):
        is_duplicate(1234)




def test_is_duplicate_non_list_int():
    with pytest.raises(TypeError):
        is_duplicate(1234)

def test_is_duplicate_non_hashable_int():
    with pytest.raises(TypeError):
        is_duplicate(1234)

def test_is_duplicate_non_list():
    with pytest.raises(TypeError):
        is_duplicate(1234)

def test_is_duplicate_non_hashable():
    with pytest.raises(TypeError):
        is_duplicate([[1, 2], [3, 4]])



def test_is_duplicate_non_list_int():
    with pytest.raises(TypeError):
        is_duplicate(1234)

def test_is_duplicate_non_hashable_int():
    with pytest.raises(TypeError):
        is_duplicate(1234)