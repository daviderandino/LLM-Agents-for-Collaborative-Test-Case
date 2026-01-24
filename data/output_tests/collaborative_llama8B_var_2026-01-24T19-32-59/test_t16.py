import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!')
])
def test_text_lowercase_underscore_match(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_empty():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_invalid():
    assert text_lowercase_underscore('Hello World123') == 'Not matched!'
    assert text_lowercase_underscore('HELLO_WORLD') == 'Not matched!'