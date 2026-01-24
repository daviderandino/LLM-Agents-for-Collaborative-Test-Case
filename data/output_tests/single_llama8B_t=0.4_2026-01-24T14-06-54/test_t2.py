import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    # Test similar elements with two tuples
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_empty():
    # Test similar elements with an empty tuple
    assert similar_elements((), ()) == ()

def test_similar_elements_single_element():
    # Test similar elements with a single element tuple
    assert similar_elements((1,), (1,)) == (1,)

def test_similar_elements_no_elements():
    # Test similar elements with two tuples that have no elements in common
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_none():
    # Test similar elements with None
    with pytest.raises(TypeError):
        similar_elements(None, (1, 2, 3))



