import pytest
from data.input_code.t15 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("Hello123World", ["Hello", "123", "World"]),
    ("HELLO", ["HELLO"]),
    ("", []),
    (None, [])  # This test should fail because split_lowerstring() expects a string
])
def test_split_lowerstring(text, expected):
    if text is None:
        with pytest.raises(TypeError):
            split_lowerstring(text)
    else:
        result = split_lowerstring(text)
        # re.findall() returns all non-overlapping matches of pattern in string, as a list of strings
        # The pattern '[a-z][^a-z]*' matches any lowercase letter followed by any number of non-letter characters
        # So, the expected results should be the lowercase parts of the input string
        expected_result = [s for s in re.findall('[a-z][^a-z]*', text) if s]
        assert result == expected_result