import pytest
from data.input_code.t2 import *

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3), (2, 3, 4), (2, 3)),
    ((), (), ()),
    ((1, 2, 2), (2, 2, 3), (2, 2)),
    ((1,), (1,), (1,)),
    ((1, 2, 3), (None, 2, 3), (2,)),
    pytest.param((1, 2, 3), ('a', 'b', 'c'), None, marks=pytest.raises(TypeError)),
    pytest.param((1, 2, 3), (1, 2), None, marks=pytest.raises(TypeError)),
])
def test_similar_elements(test_tup1, test_tup2, expected):
    if expected is None:
        with pytest.raises(TypeError):
            similar_elements(test_tup1, test_tup2)
    else:
        assert similar_elements(test_tup1, test_tup2) == expected