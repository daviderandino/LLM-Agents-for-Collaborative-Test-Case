import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    # Test similar elements in two tuples
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_empty():
    # Test similar elements when both tuples are empty
    assert similar_elements((), ()) == ()

def test_similar_elements_no_common():
    # Test similar elements when there are no common elements
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_single_element():
    # Test similar elements when both tuples have a single element
    assert similar_elements((1,), (1,)) == (1,)


def test_similar_elements_none():
    # Test similar elements with None input
    with pytest.raises(TypeError):
        similar_elements(None, (1, 2, 3))

