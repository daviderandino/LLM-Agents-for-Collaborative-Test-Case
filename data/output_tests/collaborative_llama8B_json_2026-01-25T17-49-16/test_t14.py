import pytest
from data.input_code.t14 import *



def test_find_Volume_error_non_numeric_input():
    with pytest.raises(TypeError):
        find_Volume(10, None, 30)
    with pytest.raises(TypeError):
        find_Volume(None, 20, 30)

