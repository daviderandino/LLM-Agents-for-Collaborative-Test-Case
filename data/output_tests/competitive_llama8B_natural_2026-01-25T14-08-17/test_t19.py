import pytest
from data.input_code.t19 import *

@pytest.mark.parametrize('arraynums, expected', [
    ([1, 2, 3, 4, 5], False),
    ([1, 2, 2, 3, 3, 3], True),
    ([], False),
    ([5], False),
])
def test_is_duplicate_success(arraynums, expected):
    assert is_duplicate(arraynums) == expected

def test_is_duplicate_error_none():
    with pytest.raises(TypeError):
        is_duplicate(None)



@pytest.mark.slow
def test_is_duplicate_large_array():
    arraynums = [i for i in range(100000)]
    assert is_duplicate(arraynums) == False

@pytest.mark.slow
def test_is_duplicate_very_large_array():
    arraynums = [i for i in range(1000000)]
    assert is_duplicate(arraynums) == False


def test_is_duplicate_error_non_list_instance():
    with pytest.raises(TypeError):
        is_duplicate(12345)