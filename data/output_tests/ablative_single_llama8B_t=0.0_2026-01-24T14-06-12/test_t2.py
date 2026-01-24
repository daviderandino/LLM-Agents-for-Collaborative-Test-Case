import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_success():
    # Test with two tuples containing similar elements
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_empty():
    # Test with two empty tuples
    assert similar_elements((), ()) == ()

def test_similar_elements_no_common():
    # Test with two tuples containing no common elements
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_single_element():
    # Test with two tuples containing a single common element
    assert similar_elements((1,), (1, 2)) == (1,)

def test_similar_elements_duplicates():
    # Test with two tuples containing duplicate elements
    assert similar_elements((1, 2, 2), (2, 2, 3)) == (2,)


def test_similar_elements_type_error():
    # Test with non-tuple input
    with pytest.raises(TypeError):
        similar_elements(123, (2, 3, 4))

