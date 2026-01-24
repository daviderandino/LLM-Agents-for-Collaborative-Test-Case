import pytest

from data.input_code.t2 import similar_elements



def test_zero_elements():
    test_tup1 = ()
    test_tup2 = (1, 2, 3, 4, 5)
    assert similar_elements(test_tup1, test_tup2) == (())

def test_empty_lists():
    test_tup1 = ()
    test_tup2 = ()
    assert similar_elements(test_tup1, test_tup2) == ()

def test_none_inputs():
    with pytest.raises(TypeError):
        similar_elements(None, (1, 2, 3, 4, 5))

    with pytest.raises(TypeError):
        similar_elements((1, 2, 3, 4, 5), None)

    with pytest.raises(TypeError):
        similar_elements(None, None)