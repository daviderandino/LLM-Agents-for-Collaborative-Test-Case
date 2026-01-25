import pytest
from data.input_code.t5 import count_ways




def test_count_ways_non_integer_input():
    """Test count_ways function with non-integer inputs."""
    with pytest.raises(TypeError):
        count_ways(3.5)

def test_count_ways_empty_input():
    """Test count_ways function with empty input."""
    with pytest.raises(TypeError):
        count_ways(None)

