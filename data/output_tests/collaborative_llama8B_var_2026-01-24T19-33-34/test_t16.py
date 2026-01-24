import pytest
from data.input_code.t16 import *

def test_text_lowercase_underscore_match():
    assert text_lowercase_underscore("hello_world") == "Found a match!"

def test_text_lowercase_underscore_no_match():
    assert text_lowercase_underscore("Hello World") == "Not matched!"

def test_text_lowercase_underscore_empty():
    assert text_lowercase_underscore("") == "Not matched!"

def test_text_lowercase_underscore_invalid():
    assert text_lowercase_underscore("Hello123") == "Not matched!"

def test_text_lowercase_underscore_invalid_case():
    assert text_lowercase_underscore("HELLO_WORLD") == "Not matched!"

# All tests pass, but let's improve the test code by using parametrize
import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize("input_text, expected", [
    ("hello_world", "Found a match!"),
    ("Hello World", "Not matched!"),
    ("", "Not matched!"),
    ("Hello123", "Not matched!"),
    ("HELLO_WORLD", "Not matched!"),
])
def test_text_lowercase_underscore(input_text, expected):
    assert text_lowercase_underscore(input_text) == expected