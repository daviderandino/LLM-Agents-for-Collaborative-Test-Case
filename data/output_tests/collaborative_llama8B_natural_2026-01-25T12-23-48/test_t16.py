import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!')
])
def test_text_lowercase_underscore_valid_input(text, expected):
    assert text_lowercase_underscore(text) == expected

@pytest.mark.parametrize('text, expected', [
    ('', 'Not matched!'),
    ('hello_123', 'Not matched!'),
    ('hello world', 'Not matched!')
])
def test_text_lowercase_underscore_boundary_conditions(text, expected):
    assert text_lowercase_underscore(text) == expected

def test_text_lowercase_underscore_non_string_input():
    with pytest.raises(TypeError):
        text_lowercase_underscore(123)



