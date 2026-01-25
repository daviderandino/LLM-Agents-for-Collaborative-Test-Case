import pytest
from data.input_code.t19 import *





def test_is_duplicate_large_array():
    assert is_duplicate(list(range(1000))) == False

def test_is_duplicate_non_iterable_input():
    with pytest.raises(TypeError):
        is_duplicate(123)  # Test with non-iterable integer input