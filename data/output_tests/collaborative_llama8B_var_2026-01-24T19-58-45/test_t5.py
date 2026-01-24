import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(IndexError):
        count_ways(-1)

def test_count_ways_negative_input():
    with pytest.raises(IndexError):
        count_ways(-2)


def test_count_ways_one_input():
    result = count_ways(1)
    assert result == 0









