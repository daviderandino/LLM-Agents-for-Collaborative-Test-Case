import pytest
from data.input_code.t16 import *


def test_text_lowercase_underscore_empty():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

def test_text_lowercase_underscore_none():
    with pytest.raises(TypeError):
        text_lowercase_underscore(None)

