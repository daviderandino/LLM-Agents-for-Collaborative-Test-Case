import pytest
from data.input_code.t2 import *

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (2, 3, 4), (2, 3)),
    ((1, 2, 3), (4, 5, 6), ()),
])
def test_similar_elements_success(test_tup1, test_tup2, expected):
    assert similar_elements(test_tup1, test_tup2) == expected

def test_similar_elements_none_input():
    with pytest.raises(TypeError):
        similar_elements(None, (2, 3, 4))



def test_similar_elements_non_iterable_input():
    with pytest.raises(TypeError):
        similar_elements(123, (2, 3, 4))



def test_similar_elements_none_input():
    with pytest.raises(TypeError):
        similar_elements(None, None)


def test_similar_elements_non_iterable_input():
    with pytest.raises(TypeError):
        similar_elements(123, 123)


def test_similar_elements_none_or_empty_tuple_input():
    with pytest.raises(TypeError):
        similar_elements(None, ())







