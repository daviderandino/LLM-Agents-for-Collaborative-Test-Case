import pytest
from data.input_code.t17 import square_perimeter

def test_perimeter_success():
    # Success scenario
    assert square_perimeter(1) == 4



def test_perimeter_zero():
    # Test case with zero
    assert square_perimeter(0) == 0



def test_perimeter_none():
    with pytest.raises(TypeError):
        square_perimeter(None)