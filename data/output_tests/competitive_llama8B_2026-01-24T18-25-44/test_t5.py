import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(IndexError):
        count_ways(-1)

def test_count_ways_zero():
    with pytest.raises(TypeError):
        count_ways("a")







