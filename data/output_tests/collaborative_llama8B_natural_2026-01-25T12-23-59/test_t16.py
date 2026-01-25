import pytest
from text import *

def text_lowercase_underscore(text):
    if not isinstance(text, str):
        raise TypeError("Input must be a string.")
    if '_' in text and text.islower():
        return 'Found a match!'
    else:
        return 'Not matched!'

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('hello_world123', 'Not matched!'),
    ('HelloWorld', 'Not matched!'),
    ('1hello_world', 'Not matched!'),
    ('heLlo_world', 'Not matched!'),
    ('hello@world', 'Not matched!'),
    ('', 'Not matched!')
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_none():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

def test_text_lowercase_underscore_empty_string():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)

def test_text_lowercase_underscore_non_string():
    with pytest.raises(TypeError):
        text_lowercase_underscore([1, 2, 3])