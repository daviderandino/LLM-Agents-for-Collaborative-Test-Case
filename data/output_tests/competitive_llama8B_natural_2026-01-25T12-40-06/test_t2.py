import pytest
from data.input_code.t2 import *

def test_similar_elements_happy_path():
    test_tup1 = (1, 2, 3)
    test_tup2 = (1, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == (1, 2, 3)

def test_similar_elements_no_common_elements():
    test_tup1 = (1, 2, 3)
    test_tup2 = (4, 5, 6)
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_empty_tuple():
    test_tup1 = ()
    test_tup2 = (1, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_both_empty_tuples():
    test_tup1 = ()
    test_tup2 = ()
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_duplicate_values():
    test_tup1 = (1, 2, 2, 3)
    test_tup2 = (2, 2, 4, 5)
    assert similar_elements(test_tup1, test_tup2) == (2,)


def test_similar_elements_non_hashable_values():
    test_tup1 = (1, 2, [3])
    test_tup2 = (4, 5, [6])
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)

def test_similar_elements_none_values():
    test_tup1 = (1, None, 3)
    test_tup2 = (None, 5, 6)
    assert similar_elements(test_tup1, test_tup2) == (None,)

def test_similar_elements_non_hashable_values_in_set():
    test_tup1 = (1, 2, [3])
    test_tup2 = (4, 5, [6])
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)

