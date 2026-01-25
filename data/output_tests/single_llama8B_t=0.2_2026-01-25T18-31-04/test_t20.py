import pytest
from data.input_code.t20 import multiples_of_num


def test_multiples_of_num_zero():
    """Test multiples_of_num function with zero"""
    assert multiples_of_num(0, 10) == []

def test_multiples_of_num_negative():
    """Test multiples_of_num function with negative number"""
    assert multiples_of_num(-2, 10) == []

def test_multiples_of_num_empty_list():
    """Test multiples_of_num function with empty list"""
    with pytest.raises(TypeError):
        multiples_of_num(2, [])

def test_multiples_of_num_empty_string():
    """Test multiples_of_num function with empty string"""
    with pytest.raises(TypeError):
        multiples_of_num(2, "")

def test_multiples_of_num_none():
    """Test multiples_of_num function with None"""
    with pytest.raises(TypeError):
        multiples_of_num(2, None)

def test_multiples_of_num_invalid_input_type():
    """Test multiples_of_num function with invalid input type"""
    with pytest.raises(TypeError):
        multiples_of_num("a", 10)

def test_multiples_of_num_invalid_input_type_2():
    """Test multiples_of_num function with invalid input type"""
    with pytest.raises(TypeError):
        multiples_of_num(2, "a")