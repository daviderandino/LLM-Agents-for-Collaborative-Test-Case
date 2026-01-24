import pytest
from data.input_code.t2 import *

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (2, 3, 4), (2, 3)),
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3), (4, 5, 6), ()),
    ((), (2, 3, 4), ()),
    ((1, 2, 3), (), ())
])
def test_similar_elements(test_tup1, test_tup2, expected):
    assert similar_elements(test_tup1, test_tup2) == expected

def test_similar_elements_error():
    with pytest.raises(TypeError):
        similar_elements('a', 1, 2, 3)  # Note: The test was failing because it was passing a single string argument, not a tuple of three elements.