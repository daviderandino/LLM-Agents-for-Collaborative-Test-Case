import pytest
from data.input_code.t2 import similar_elements

def test_similar_elements_two_equal_tuples():
    test_tup1 = (1, 2, 2, 3)
    test_tup2 = (2, 2, 3, 4)
    assert similar_elements(test_tup1, test_tup2) == (2, 2, 3)

def test_similar_elements_two_different_lists():
    test_tup1 = (1, 2, 2, 3)
    test_tup2 = [2, 4, 5]
    assert similar_elements(test_tup1, test_tup2) == (2,)

def test_similar_elements_two_empty_tuples():
    test_tup1 = ()
    test_tup2 = ()
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_no_common_elements():
    test_tup1 = (1, 2, 3, 4)
    test_tup2 = (5, 6, 7, 8)
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_none_input():
    test_tup1 = None
    test_tup2 = (1, 2, 3, 4)
    with pytest.raises AttributeError:
        similar_elements(test_tup1, test_tup2)

def test_similar_elements_input_tuples_with_zero():
    test_tup1 = (0, 1, 2, 3)
    test_tup2 = (0, 4, 5, 6)
    assert similar_elements(test_tup1, test_tup2) == (0,)

def test_similar_elements_input_tuples_with_negative():
    test_tup1 = (-1, -2, -2, -3)
    test_tup2 = (-2, -2, -3, -4)
    assert similar_elements(test_tup1, test_tup2) == (-2, -2, -3)

def test_similar_elements_input_tuples_with_maxsize():
    import sys
    test_tup1 = tuple(range(sys.maxsize))
    test_tup2 = tuple(range(sys.maxsize))
    assert similar_elements(test_tup1, test_tup2) == test_tup1

def test_similar_elements_input_tuples_with_minsize():
    import sys
    test_tup1 = tuple(range(sys.minsize))
    test_tup2 = tuple(range(sys.minsize))
    assert similar_elements(test_tup1, test_tup2) == test_tup1

def test_similar_elements_maxsize_minus_one_input():
    import sys
    test_tup1 = tuple(range(sys.maxsize - 1))
    test_tup2 = tuple(range(sys.maxsize - 1))
    assert similar_elements(test_tup1, test_tup2) == test_tup1

def test_similar_elements_maxsize_plus_one_input():
    import sys
    test_tup1 = tuple(range(sys.maxsize))
    test_tup2 = tuple(range(sys.maxsize + 1))
    assert similar_elements(test_tup1, test_tup2) == test_tup1

def test_similar_elements_empty_string_input():
    with pytest.raises TypeError:
        similar_elements("hello", (1, 3, 4, 7))