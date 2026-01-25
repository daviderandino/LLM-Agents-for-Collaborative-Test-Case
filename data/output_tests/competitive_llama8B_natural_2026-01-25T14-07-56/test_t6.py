import pytest
from data.input_code.t6 import *

@pytest.mark.parametrize('a, expected', [
    (8, True),
    (10, False)
])
def test_is_Power_Of_Two_success(a, expected):
    assert is_Power_Of_Two(a) == expected

def test_is_Power_Of_Two_zero():
    assert is_Power_Of_Two(0) == False

def test_is_Power_Of_Two_one():
    assert is_Power_Of_Two(1) == True

def test_is_Power_Of_Two_negative():
    assert is_Power_Of_Two(-8) == False


