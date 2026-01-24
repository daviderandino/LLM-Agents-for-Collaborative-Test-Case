import pytest
from data.input_code.t7 import find_char_long




def test_find_char_long_empty_string():
    result = find_char_long("")
    assert result == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_empty_list():
    with pytest.raises(TypeError):
        find_char_long([])

def test_find_char_long_invalid_input():
    with pytest.raises(TypeError):
        find_char_long(123)