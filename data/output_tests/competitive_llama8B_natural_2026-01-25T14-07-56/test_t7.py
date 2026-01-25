import pytest
from data.input_code.t7 import *

def test_find_char_long_normal_text():
    assert find_char_long("Hello World, this is a test") == ['Hello', 'World', 'this', 'test']

def test_find_char_long_text_with_numbers():
    assert find_char_long("Hello123 World, this is a test") == ['Hello123', 'World', 'this', 'test']

def test_find_char_long_text_with_punctuation():
    assert find_char_long("Hello, World! this is a test") == ['Hello', 'World', 'this', 'test']


def test_find_char_long_multi_word():
    assert find_char_long("Hello World this test") == ['Hello', 'World', 'this', 'test']

def test_find_char_long_empty_text():
    assert find_char_long("") == []

def test_find_char_long_none_input():
    with pytest.raises(TypeError):
        find_char_long(None)

def test_find_char_long_special_characters():
    assert find_char_long("Hello, World! @#$") == ['Hello', 'World']

# The function is supposed to find words with 4 or more characters, so 'Hello' and 'World' should be found
# but 'this' and 'test' should not because they have less than 4 characters
def test_find_char_long_single_word_with_numbers():
    assert find_char_long("Hello123") == ['Hello123']


