import pytest
from data.input_code.t15 import *

@pytest.mark.parametrize('text, expected', [
    ("Hello World", ["Hello", "World"]),
    ("Hello123", ["Hello", "123"]),
    ("HELLO", []),
    ("", []),
    (None, [])
])
def test_split_lowerstring(text, expected):
    if text is None:
        with pytest.raises(TypeError):
            split_lowerstring(text)
    else:
        result = split_lowerstring(text)
        if expected == []:
            assert result == []
        else:
            assert all(re.match('^[a-z][^a-z]*$', s) for s in result) and result == [s for s in result if s[0].islower()]