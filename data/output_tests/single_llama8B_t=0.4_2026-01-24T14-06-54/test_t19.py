import pytest
from data.input_code.t19 import is_duplicate

@pytest.mark.parametrize("arraynums, expected", [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 3, 4], True),
    ([1, 1, 1, 1, 1], True),
    ([], False),
    ([1], False),
    ([1, 1], True),
    ([1, 2, 3, 4, 5, 6], False),
])
def test_test_duplicate(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_test_duplicate_empty_set():
    with pytest.raises(TypeError):
        is_duplicate(None)


