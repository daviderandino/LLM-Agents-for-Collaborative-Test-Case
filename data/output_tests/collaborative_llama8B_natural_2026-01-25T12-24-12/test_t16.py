import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('HelloWorld', 'Not matched!')
])
def test_text_lowercase_underscore_match(text, expected):
    assert text_lowercase_underscore(text) == expected

@pytest.mark.parametrize('text, expected', [
    ('', 'Not matched!'),
    ('hello_123', 'Not matched!'),
    ('hello world', 'Not matched!'),
    ('HELLO_WORLD', 'Not matched!'),
    ('123_456', 'Not matched!')
])
def test_text_lowercase_underscore_non_match(text, expected):
    assert text_lowercase_underscore(text) == expected