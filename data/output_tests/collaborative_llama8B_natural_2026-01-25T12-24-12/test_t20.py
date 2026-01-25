import pytest
from data.input_code.t20 import *

def test_multiples_of_num_success():
    assert multiples_of_num(10, 2) == [2, 4, 6, 8, 10, 12, 14, 16, 18, 20]



def test_multiples_of_num_negative_range():
    assert multiples_of_num(-10, 2) == []