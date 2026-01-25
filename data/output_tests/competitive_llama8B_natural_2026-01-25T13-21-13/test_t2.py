import pytest
from data.input_code.t2 import *

def test_similar_elements_identical():
    assert similar_elements((1,2,3), (1,2,3)) == (1,2,3)

def test_similar_elements_partially_identical():
    assert similar_elements((1,2,3), (1,2,4)) == (1,2)

def test_similar_elements_empty():
    assert similar_elements((), ()) == ()

def test_similar_elements_single_element():
    assert similar_elements((1,), (1,)) == (1,)

def test_similar_elements_duplicates():
    assert similar_elements((1,2,2), (2,2,3)) == (2,)

def test_similar_elements_non_unique():
    assert similar_elements((1,2,3), (1,2,3,4)) == (1,2,3)

def test_similar_elements_length_mismatch():
    assert similar_elements((1,2,3), (1,2)) == (1,2)

def test_similar_elements_non_hashable():
    with pytest.raises(TypeError):
        similar_elements((1, ['a']), (1, ['a']))


def test_similar_elements_none_input():
    with pytest.raises(TypeError):
        similar_elements(None, (1,2,3))

