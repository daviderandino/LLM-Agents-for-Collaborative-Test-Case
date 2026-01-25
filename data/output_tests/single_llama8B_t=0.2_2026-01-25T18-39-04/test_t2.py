import pytest

from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    test_tup1 = (1, 2, 3, 4, 5)
    test_tup2 = (4, 5, 6, 7, 8)
    assert similar_elements(test_tup1, test_tup2) == (4, 5)

def test_similar_elements_empty():
    test_tup1 = ()
    test_tup2 = (1, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_single_element():
    test_tup1 = (1,)
    test_tup2 = (1, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == (1,)

def test_similar_elements_no_common_elements():
    test_tup1 = (1, 2, 3)
    test_tup2 = (4, 5, 6)
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_none():
    test_tup1 = None
    test_tup2 = (1, 2, 3)
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)


def test_similar_elements_non_hashable():
    test_tup1 = ([1, 2], 3, 4)
    test_tup2 = (1, 2, 3)
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)