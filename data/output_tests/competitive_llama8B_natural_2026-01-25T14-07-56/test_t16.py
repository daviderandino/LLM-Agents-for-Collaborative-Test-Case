import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('hello world', 'Not matched!'),
    ('Hello_World', 'Not matched!'),
    ('hello world', 'Not matched!'),
    ('a', 'Not matched!'),
    ('a_b', 'Found a match!'),
    ('', 'Not matched!')
])
def test_text_lowercase_underscore_valid(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_invalid_uppercase():
    assert text_lowercase_underscore('Hello_World') == 'Not matched!'

def test_text_lowercase_underscore_invalid_no_underscores():
    assert text_lowercase_underscore('Hello World') == 'Not matched!'

def test_text_lowercase_underscore_empty():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_none():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)