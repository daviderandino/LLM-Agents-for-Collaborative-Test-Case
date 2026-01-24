import pytest
from data.input_code.t2 import *

def test_similar_elements_ok():
    assert similar_elements((1, 2, 3), (2, 3, 4)) == (2, 3)

def test_similar_elements_no_common_elements():
    assert similar_elements((1, 2, 3), (4, 5, 6)) == ()

def test_similar_elements_none_input():
    with pytest.raises(TypeError):
        similar_elements(None, (2, 3, 4))

def test_similar_elements_none_input2():
    with pytest.raises(TypeError):
        similar_elements((1, 2, 3), None)






def test_similar_elements_empty_list():
    assert similar_elements([], []) == ()

def test_similar_elements_empty_tuple():
    assert similar_elements((), ()) == ()

def test_similar_elements_single_element():
    assert similar_elements((1,), (1,)) == (1,)

def test_similar_elements_single_element_no_match():
    assert similar_elements((1,), (2,)) == ()