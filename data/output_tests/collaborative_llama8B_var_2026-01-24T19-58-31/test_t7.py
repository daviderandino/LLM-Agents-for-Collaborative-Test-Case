import pytest
from data.input_code.t7 import *


def test_find_char_long_no_matches():
    result = find_char_long("Hello")
    assert result == ["Hello"]  # Corrected the expected result

def test_find_char_long_empty_string():
    result = find_char_long("")
    assert result == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)