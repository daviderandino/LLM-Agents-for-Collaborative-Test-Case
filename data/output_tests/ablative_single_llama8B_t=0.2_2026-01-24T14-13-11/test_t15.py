import pytest
from data.input_code.t15 import split_lowerstring

def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []














def test_split_lowerstring_string_with_non_string_input():
    with pytest.raises(TypeError):
        split_lowerstring(123)