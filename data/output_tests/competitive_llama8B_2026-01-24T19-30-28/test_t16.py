import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!'),
    ('', 'Not matched!')
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_invalid():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)