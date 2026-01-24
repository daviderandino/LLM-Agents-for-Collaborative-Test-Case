import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_lower_string():
    assert split_lowerstring("hello") == ['h','e','l','l','o']




def test_split_lowerstring_invalid_input_type():
    with pytest.raises(TypeError):
        split_lowerstring(123)

