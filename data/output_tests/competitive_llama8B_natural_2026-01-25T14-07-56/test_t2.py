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

def test_similar_elements_partial_match():
    test_tup1 = (1, 2, 3)
    test_tup2 = (2, 3, 4)
    assert similar_elements(test_tup1, test_tup2) == (2, 3)

def test_similar_elements_single_element_match():
    test_tup1 = (1,)
    test_tup2 = (1,)
    assert similar_elements(test_tup1, test_tup2) == (1,)

def test_similar_elements_truncation():
    test_tup1 = (1, 2)
    test_tup2 = (1, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == (1, 2)

def test_similar_elements_empty_tuples():
    test_tup1 = ()
    test_tup2 = ()
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_duplicates():
    test_tup1 = (1, 2, 2)
    test_tup2 = (2, 2, 3)
    assert similar_elements(test_tup1, test_tup2) == (2,)

def test_similar_elements_non_hashable_elements():
    test_tup1 = (1, [2], 3)
    test_tup2 = (1, [2], 3)
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)

def test_similar_elements_none_input():
    test_tup1 = None
    test_tup2 = (1,)
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)

