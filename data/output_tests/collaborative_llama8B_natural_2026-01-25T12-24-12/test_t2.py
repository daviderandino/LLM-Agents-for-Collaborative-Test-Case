import pytest
from data.input_code.t2 import similar_elements

@pytest.mark.parametrize('test_tup1, test_tup2, expected', [
    ((1, 2, 3), (1, 2, 3), (1, 2, 3)),
    ((1, 2, 3), (2, 3, 4), (2, 3)),
    ((1, 2, 3), (4, 5, 6), ()),
    ((), (), ()),
    ((1, 2, 3), ()), (),
    ((1, 2, 2), (2, 2, 3), (2,)),
    ((1, [1, 2]), (1, [1, 2])), pytest.raises(TypeError),
    ((1, None), (1, None)), (1, None),
    ((1, 2**63), (2**63, 3)), (2**63,),
    ((-1, 2), (-1, 3)), (-1,)
])
def test_similar_elements(test_tup1, test_tup2, expected):
    if expected == ():
        assert similar_elements(test_tup1, test_tup2) == expected
    elif expected == pytest.raises(TypeError):
        with pytest.raises(TypeError):
            similar_elements(test_tup1, test_tup2)
    else:
        assert similar_elements(test_tup1, test_tup2) == expected