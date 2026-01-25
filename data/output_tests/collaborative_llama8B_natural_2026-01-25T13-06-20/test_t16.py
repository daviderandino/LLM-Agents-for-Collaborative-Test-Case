import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('hello_123', 'Not matched!'),
    ('hello world', 'Not matched!'),
    ('hello', 'Not matched!'),
    ('', 'Not matched!'),
    ('123hello_world', 'Not matched!'),
    ('Hello_world', 'Not matched!')
])
def test_text_lowercase_underscore_valid(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_invalid():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

def test_text_lowercase_underscore_all_uppercase():
    assert text_lowercase_underscore('HELLO_WORLD') == 'Not matched!'