import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 4, 5], True),
    ([], False),
    ([1], False),
    (None, TypeError)
])
def test_is_duplicate(arraynums, expected):
    if isinstance(expected, type) and issubclass(expected, Exception):
        with pytest.raises(expected):
            is_duplicate(arraynums)
    else:
        assert is_duplicate(arraynums) == expected