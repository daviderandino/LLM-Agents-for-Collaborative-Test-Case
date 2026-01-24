import pytest
from data.input_code.t7 import *


def test_find_char_long_error():
    with pytest.raises(TypeError):
        find_char_long(None)