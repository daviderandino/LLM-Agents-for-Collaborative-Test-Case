import pytest
from data.input_code.t8 import *


def test_square_nums_error():
    with pytest.raises(TypeError):
        square_nums([1, 'a', 3, 4, 5])