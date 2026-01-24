import pytest
from data.input_code.t5 import *
from math import comb



@pytest.mark.parametrize('n', [
    'a',
    3.5,
    None
])
def test_count_ways_invalid_type_error(n):
    with pytest.raises(TypeError):
        count_ways(n)


