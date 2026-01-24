import pytest
from data.input_code.t19 import *


def test_is_duplicate_none():
    with pytest.raises(TypeError):
        is_duplicate(None)

def test_is_duplicate_non_list():
    with pytest.raises(TypeError):
        is_duplicate(12345)