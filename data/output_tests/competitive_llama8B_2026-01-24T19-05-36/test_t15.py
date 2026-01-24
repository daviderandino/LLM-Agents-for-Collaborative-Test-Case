import pytest
from data.input_code.t15 import *




def test_split_lowerstring_empty_string():
    # Test ''
    text = ""
    expected = []
    result = split_lowerstring(text)
    assert result == expected

def test_split_lowerstring_none():
    # Test 'None'
    text = None
    with pytest.raises(TypeError):
        split_lowerstring(text)