import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!')
])
def test_text_lowercase_underscore_valid(text, expected):
    assert text_lowercase_underscore(text) == expected

@pytest.mark.parametrize('text, expected', [
    ('hello_123_world', 'Not matched!'),
    ('HeLlO_WoRlD', 'Not matched!'),
    ('hello_123_world', 'Not matched!'),
    ('', 'Not matched!'),
    ('çàà', 'Not matched!'),
    ('hello world', 'Not matched!'),
    ('hello!', 'Not matched!')
])
def test_text_lowercase_underscore_invalid(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_non_string():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)