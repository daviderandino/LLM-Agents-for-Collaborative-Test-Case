import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 4, 5], True),
    ([], False),
    ([None], False)
])
def test_is_duplicate(arraynums, expected):
    assert is_duplicate(arraynums) == expected