import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    # Test with two tuples containing similar elements
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_empty():
    # Test with two empty tuples
    assert similar_elements((), ()) == ()

def test_similar_elements_no_overlap():
    # Test with two tuples containing no similar elements
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_single_element():
    # Test with two tuples containing a single similar element
    assert similar_elements((1,), (1, 2)) == (1,)



