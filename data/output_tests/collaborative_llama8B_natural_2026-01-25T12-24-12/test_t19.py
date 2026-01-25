import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 3, 3, 3], True),
    ([], False),
    ([5], False),
    ([1, 2], False),
    ([1, 2, 2, None], True),
])
def test_is_duplicate(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_non_hashable():
    with pytest.raises(TypeError):
        is_duplicate([1, ['a'], ['a']])