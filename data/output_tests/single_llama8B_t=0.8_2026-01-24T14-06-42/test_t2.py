import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    result = similar_elements((1, 2, 3), (2, 3, 4))
    assert result == (2, 3)

def test_similar_elements_empty_elements():
    result = similar_elements((1, 2, 3), tuple())
    assert result == ()

def test_similar_elements_no_similar_elements():
    result = similar_elements((1, 2, 3), (4, 5, 6))
    assert result == ()


def test_similar_elements_empty_list():
    result = similar_elements(tuple(), (2, 2, 3))
    assert result == ()




def test_similar_elements_single_element():
    result = similar_elements((1,), (1, 2, 3))
    assert result == (1,)





