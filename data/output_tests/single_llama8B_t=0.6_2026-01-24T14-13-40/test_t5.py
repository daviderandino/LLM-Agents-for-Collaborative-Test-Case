import pytest
from data.input_code.t5 import count_ways



def test_count_ways_invalid_input():
    # Test invalid input
    with pytest.raises(TypeError):
        count_ways("a")
    with pytest.raises(TypeError):
        count_ways(1.5)