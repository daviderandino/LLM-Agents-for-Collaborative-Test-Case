import pytest
from data.input_code.t7 import find_char_long


def test_find_char_long_empty_string():
    text = ""
    expected_result = []
    assert find_char_long(text) == expected_result


def test_find_char_long_empty_list():
    text = "   "
    expected_result = []
    assert find_char_long(text) == expected_result

def test_find_char_long_non_string_input():
    text = 12345
    with pytest.raises(TypeError):
        find_char_long(text)

def test_find_char_long_invalid_input():
    text = None
    with pytest.raises(TypeError):
        find_char_long(text)