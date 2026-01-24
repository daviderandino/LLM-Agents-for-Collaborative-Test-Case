import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 4, 5], True),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected


def test_is_duplicate_none():
    with pytest.raises(TypeError):
        is_duplicate(None)







def test_is_duplicate_non_iterable():
    with pytest.raises(TypeError):
        is_duplicate(12345)