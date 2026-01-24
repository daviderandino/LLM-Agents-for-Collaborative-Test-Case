import pytest
from data.input_code.t15 import *


def test_split_lowerstring_error():
    with pytest.raises(TypeError):
        split_lowerstring(None)