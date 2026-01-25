import pytest
from data.input_code.t7 import *

@pytest.mark.parametrize('text, expected', [
    ("hello world", ["hello", "world"]),
    ("abcde", ["abcde"]),
    ("abc", []),
    ("", [])
])
def test_find_char_long_success(text, expected):
    assert find_char_long(text) == expected

def test_find_char_long_none():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_non_string():
    with pytest.raises(TypeError):
        find_char_long(123)