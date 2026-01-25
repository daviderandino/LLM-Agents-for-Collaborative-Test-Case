import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('HelloWorld', 'Not matched!')
])
def test_text_lowercase_underscore_pattern_match(text, expected):
    assert text_lowercase_underscore(text) == expected


def test_text_lowercase_underscore_empty_input():
    assert text_lowercase_underscore('') == 'Not matched!'

def test_text_lowercase_underscore_none_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

