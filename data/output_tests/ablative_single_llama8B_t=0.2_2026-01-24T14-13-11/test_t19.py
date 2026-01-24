import pytest
from data.input_code.t19 import is_duplicate



def test_duplicate_empty_array():
    arraynums = []
    assert is_duplicate(arraynums) == False

def test_duplicate_single_element_array():
    arraynums = [1]
    assert is_duplicate(arraynums) == False

def test_duplicate_none_input():
    with pytest.raises(TypeError):
        is_duplicate(None)

