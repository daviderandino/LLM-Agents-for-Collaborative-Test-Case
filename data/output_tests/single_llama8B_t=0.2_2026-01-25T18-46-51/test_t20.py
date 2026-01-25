import pytest
from data.input_code.t20 import multiples_of_num


def test_multiples_of_num_edge_case_m_zero():
    """Test multiples_of_num function with m as zero."""
    assert multiples_of_num(0, 5) == []






def test_multiples_of_num_invalid_input_type():
    """Test multiples_of_num function with invalid input types."""
    with pytest.raises(TypeError):
        multiples_of_num("a", 5)
    with pytest.raises(TypeError):
        multiples_of_num(2, "b")