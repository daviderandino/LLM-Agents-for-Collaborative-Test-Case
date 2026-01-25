import pytest

from data.input_code.t5 import count_ways


def test_count_ways_one():
    assert count_ways(1) == 0



def test_count_ways_non_integer():
    with pytest.raises(TypeError):
        count_ways(1.5)


