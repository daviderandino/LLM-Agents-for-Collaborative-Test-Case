import pytest
from data.input_code.t7 import find_char_long


def test_find_char_long_empty_string():
    text = ""
    result = find_char_long(text)
    assert result == []



def test_find_char_long_none_input():
    text = None
    with pytest.raises(TypeError):
        find_char_long(text)






def test_find_char_long_non_string_input():
    text = 123
    with pytest.raises(TypeError):
        find_char_long(text)