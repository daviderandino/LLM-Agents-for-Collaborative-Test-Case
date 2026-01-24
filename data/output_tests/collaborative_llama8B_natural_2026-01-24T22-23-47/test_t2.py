import pytest
from data.input_code.t2 import *

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3), (4, 5, 6), ()),
    ((1, 2, 3), (2, 3, 4), (2, 3)),
    ((3, 2, 1), (1, 2, 3), (1, 2, 3)),
    ((), (1, 2, 3), ()),
    ((1, 2, 3), (), ()),
])
def test_similar_elements(test_tup1, test_tup2, expected):
    assert similar_elements(test_tup1, test_tup2) == expected

def test_similar_elements_empty_input():
    assert similar_elements((), ()) == ()

def test_similar_elements_none_input():
    with pytest.raises(TypeError):
        similar_elements(None, (1, 2, 3))




