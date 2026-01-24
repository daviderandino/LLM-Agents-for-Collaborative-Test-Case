import pytest
from data.input_code.t20 import multiples_of_num






def test_multiples_of_num_zero():
    """Test multiples_of_num function with zero value."""
    assert multiples_of_num(0, 10) == []

def test_multiples_of_num_none():
    """Test multiples_of_num function with None value."""
    with pytest.raises(TypeError):
        multiples_of_num(None, 10)

