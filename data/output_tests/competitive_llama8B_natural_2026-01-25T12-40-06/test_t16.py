import pytest
from data.input_code.t16 import *
from re import search

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!'),
    ('', 'Not matched!'),
    ('_hello', 'Not matched!'),
    ('Hello_world', 'Not matched!'),
    ('hello123', 'Not matched!'),
    ('hello!', 'Not matched!'),
    ('hello_world!', 'Not matched!'),
    ('hello__world', 'Not matched!')
])
def test_text_lowercase_underscore_success(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_pattern_violation():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)

