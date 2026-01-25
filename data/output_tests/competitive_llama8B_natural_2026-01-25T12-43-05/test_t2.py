import pytest
from data.input_code.t2 import *

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3, 4), (2, 3, 4, 5), (2, 3, 4)),
    ((1, 2, 3), (4, 5, 6), ()),
    ((1, 2, 3), (2, 3), (2, 3)),
    ((1, 2, 2, 3), (2, 3), (2, 3)),
    ((), (), ()),
    ((), (1, 2, 3), ()),
    ((1, 2, 3), {2, 3}, (2, 3)),
    ([1, 2, 3], [2, 3, 4], (2, 3)),
    ((1, 2, 3), None, TypeError)
])
def test_similar_elements(test_tup1, test_tup2, expected):
    if isinstance(expected, type):
        with pytest.raises(expected):
            similar_elements(test_tup1, test_tup2)
    else:
        assert similar_elements(test_tup1, test_tup2) == expected