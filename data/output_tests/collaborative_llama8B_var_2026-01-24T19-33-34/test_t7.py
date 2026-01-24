import pytest
from data.input_code.t7 import *


# Additional test case to cover the failing assertion
@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
])
def test_find_char_long_additional(text, expected):
    result = find_char_long(text)
    assert result == expected