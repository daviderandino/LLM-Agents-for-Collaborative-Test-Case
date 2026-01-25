import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('HELLO_WORLD', 'Not matched!'),
    ('', 'Not matched!')
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_no_underscore():
    assert text_lowercase_underscore('hello') == 'Not matched!'

def test_text_lowercase_underscore_no_lowercase():
    assert text_lowercase_underscore('HELLO') == 'Not matched!'