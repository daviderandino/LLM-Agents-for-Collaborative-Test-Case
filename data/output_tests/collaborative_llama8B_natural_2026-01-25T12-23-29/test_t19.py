import pytest
from data.input_code.t19 import *


def test_is_duplicate_non_hashable():
    with pytest.raises(TypeError):
        is_duplicate([[1, 2], [1, 2]])



