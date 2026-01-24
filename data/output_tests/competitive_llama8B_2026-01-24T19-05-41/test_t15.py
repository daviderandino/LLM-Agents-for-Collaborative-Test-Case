import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_string():
    with pytest.raises(TypeError):
        split_lowerstring(None)

def test_split_lowerstring_empty_input():
    result = split_lowerstring("")
    assert isinstance(result, list) and len(result) == 0