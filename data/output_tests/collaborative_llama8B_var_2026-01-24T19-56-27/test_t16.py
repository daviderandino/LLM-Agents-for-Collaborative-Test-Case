import pytest
from data.input_code.t16 import *

@pytest.mark.parametrize('text, expected', [
    ('hello_world', 'Found a match!'),
    ('Hello World', 'Not matched!'),
    ('Hello_World', 'Not matched!'),
    ('hello', 'Not matched!'),
    ('hello_world123', 'Not matched!'),
    ('', 'Not matched!'),
    (None, 'Not matched!'),  # This test case should pass because it doesn't match the pattern
    (123, 'Not matched!')    # This test case should pass because it doesn't match the pattern
])
def test_text_lowercase_underscore(text, expected):
    if text is None or not isinstance(text, str):  # Check if text is not a string
        assert text_lowercase_underscore(text) == 'Not matched!'
    else:
        patterns = '^[a-z]+_[a-z]+$'
        result = text_lowercase_underscore(text)
        assert result == expected  # Directly compare result with expected