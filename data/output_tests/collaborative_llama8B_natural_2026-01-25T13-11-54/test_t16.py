import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore('hello_world') == 'Found a match!'
    assert text_lowercase_underscore('HelloWorld') == 'Not matched!'

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('HelloWorld', 'Not matched!'),
    ('hello_world!', 'Not matched!'),
    ('hello_1world', 'Not matched!'),
    ('', 'Not matched!'),
    ('Hello_world', 'Not matched!'),
    ('hëllo_world', 'Not matched!')
])
def test_text_lowercase_underscore_mismatch(text, expected):
    assert text_lowercase_underscore(text) == expected

@pytest.mark.parametrize('text, expected', [
    ('hello__world', 'Not matched!'),
    ('_hello_world', 'Not matched!')
])
def test_text_lowercase_underscore_edge_cases(text, expected):
    assert text_lowercase_underscore(text) == expected

