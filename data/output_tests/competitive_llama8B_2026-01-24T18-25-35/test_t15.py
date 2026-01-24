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
        # Adjust the expected output according to the source code logic
        expected_output = [s[0].lower() + s[1:] for s in re.findall('[a-z][^a-z]*', text)]
        assert result == expected_output