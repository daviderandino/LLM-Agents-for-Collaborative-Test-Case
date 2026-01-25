import pytest
from data.input_code.t20 import *



def test_multiples_of_num_zero_multiplicand():
    with pytest.raises(ValueError):
        multiples_of_num(3, 0)



def test_multiples_of_num_success_with_corrected_assertion():
    assert multiples_of_num(10, 5) == [5, 10, 15, 20, 25, 30, 35, 40, 45, 50]



