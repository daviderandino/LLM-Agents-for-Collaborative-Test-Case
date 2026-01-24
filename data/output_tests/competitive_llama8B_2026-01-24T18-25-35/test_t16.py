import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!'),
    ('', 'Not matched!'),
    ('Hello World!', 'Not matched!'),
    ('Hello World123', 'Not matched!')
])
def test_text_lowercase_underscore(text, expected):
    assert text_lowercase_underscore(text) == expected