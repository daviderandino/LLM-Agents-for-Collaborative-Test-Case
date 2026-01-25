import pytest
from data.input_code.t2 import similar_elements

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3), (4, 5, 6), ()),
    ((1, 2, 2, 3), (2, 2, 3, 4), (2, 2, 3)),
    ((), (), ()),
    ((1, 2, 3), (), ()),
    (None, (1, 2, 3), None),
    ([1, 2, 3], (1, 2, 3), None),
    ((1, 2, list(3)), (1, 2, 3), None),
])
def test_similar_elements(test_tup1, test_tup2, expected):
    if expected is None:
        with pytest.raises((TypeError, ValueError)):
            similar_elements(test_tup1, test_tup2)
    else:
        try:
            assert similar_elements(test_tup1, test_tup2) == expected
        except Exception as e:
            pytest.fail(f"similar_elements returned unexpected result: {e}")