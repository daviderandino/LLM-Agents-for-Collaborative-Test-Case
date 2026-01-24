import pytest
from data.input_code.t20 import multiples_of_num



def test_multiples_of_num_error_handling():
    """Test multiples_of_num function with error handling."""
    with pytest.raises(TypeError):
        multiples_of_num("a", 5)
    with pytest.raises(TypeError):
        multiples_of_num(2, "b")
    with pytest.raises(TypeError):
        multiples_of_num("a", "b")

