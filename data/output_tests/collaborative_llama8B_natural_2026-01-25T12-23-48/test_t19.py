import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 3, 3], True),
    ([], False),
    ([1], False),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_empty_array():
    with pytest.raises(TypeError):
        is_duplicate(None)



def test_is_duplicate_mixed_numeric_types():
    assert is_duplicate([1, 2.0, 3]) == False


