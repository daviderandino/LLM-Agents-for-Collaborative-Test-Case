import pytest
from data.input_code.t8 import *

def test_square_nums_large():
    result = square_nums([i for i in range(100)])
    assert len(result) == 100
    assert result[0] == 0
    assert result[-1] == 9801