import pytest

from data.input_code.t2 import similar_elements


def test_similar_elements_empty():
    test_tup1 = ()
    test_tup2 = ()
    assert similar_elements(test_tup1, test_tup2) == ()

def test_similar_elements_no_common():
    test_tup1 = (1, 2, 3)
    test_tup2 = (4, 5, 6)
    assert similar_elements(test_tup1, test_tup2) == ()


def test_similar_elements_none():
    test_tup1 = None
    test_tup2 = (1, 2, 3)
    with pytest.raises(TypeError):
        similar_elements(test_tup1, test_tup2)



