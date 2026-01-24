import pytest
from data.input_code.t19 import test_duplicate



def test_duplicate_empty_array():
    arraynums = []
    assert test_duplicate(arraynums) == False

def test_duplicate_single_element_array():
    arraynums = [1]
    assert test_duplicate(arraynums) == False

def test_duplicate_none_input():
    with pytest.raises(TypeError):
        test_duplicate(None)

