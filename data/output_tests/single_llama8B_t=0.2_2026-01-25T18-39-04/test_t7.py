import pytest
from data.input_code.t7 import find_char_long


def test_find_char_long_empty_string():
    text = ""
    expected = []
    assert find_char_long(text) == expected




def test_find_char_long_invalid_input():
    with pytest.raises(TypeError):
        find_char_long(123)

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_empty_list_input():
    with pytest.raises(TypeError):
        find_char_long([])