import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_string():
    assert split_lowerstring("") == []

def test_split_lowerstring_none_input():
    with pytest.raises(TypeError):
        split_lowerstring(None)






