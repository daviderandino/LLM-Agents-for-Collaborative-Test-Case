import pytest
from data.input_code.t7 import *


def test_find_char_long_empty_input():
    with pytest.raises(TypeError):
        find_char_long(None)


def test_find_char_long_empty_string():
    result = find_char_long("")
    assert result == []