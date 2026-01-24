import pytest

from data.input_code.t5 import count_ways



def test_count_ways_non_integer():
    # Test case for non-integer values (should raise TypeError)
    with pytest.raises(TypeError):
        count_ways(3.5)



