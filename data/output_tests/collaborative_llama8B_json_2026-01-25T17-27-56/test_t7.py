import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("hello world", ["hello", "world"]),
    ("abcdef", ["abcdef"]),
    ("abc", []),
    ("abc123", ["abc123"]),
])
def test_find_char_long_success(text, expected):
    assert find_char_long(text) == expected

def test_find_char_long_empty_string():
    assert find_char_long("") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)