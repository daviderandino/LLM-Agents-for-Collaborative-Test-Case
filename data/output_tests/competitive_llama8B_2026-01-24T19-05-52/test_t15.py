import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_string():
    with pytest.raises(TypeError):
        split_lowerstring(None)


def test_split_lowerstring_single_char():
    result = split_lowerstring("a")
    assert result == ["a"]


