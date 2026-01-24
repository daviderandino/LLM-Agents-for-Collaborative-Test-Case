import pytest
from data.input_code.t8 import square_nums

def test_square_nums_success():
    """Test square_nums function with a list of numbers."""
    nums = [1, 2, 3, 4, 5]
    result = square_nums(nums)
    assert result == [1, 4, 9, 16, 25]

def test_square_nums_empty_list():
    """Test square_nums function with an empty list."""
    nums = []
    result = square_nums(nums)
    assert result == []

def test_square_nums_single_element():
    """Test square_nums function with a single element list."""
    nums = [10]
    result = square_nums(nums)
    assert result == [100]

def test_square_nums_negative_numbers():
    """Test square_nums function with negative numbers."""
    nums = [-1, -2, -3]
    result = square_nums(nums)
    assert result == [1, 4, 9]

def test_square_nums_zero():
    """Test square_nums function with zeros."""
    nums = [0]
    result = square_nums(nums)
    assert result == [0]

def test_square_nums_none_input():
    """Test square_nums function with None input."""
    with pytest.raises(TypeError):
        square_nums(None)