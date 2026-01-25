import pytest

from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    # Test with similar elements
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_empty():
    # Test with empty tuples
    assert similar_elements((), ()) == ()

def test_similar_elements_no_common():
    # Test with no common elements
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_single_element():
    # Test with single element tuples
    assert similar_elements((1,), (1,)) == (1,)

def test_similar_elements_none():
    # Test with None input
    with pytest.raises(TypeError):
        similar_elements(None, (1, 2, 3))


