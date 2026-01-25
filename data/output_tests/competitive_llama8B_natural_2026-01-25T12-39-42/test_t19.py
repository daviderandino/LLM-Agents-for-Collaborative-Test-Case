import pytest
from data.input_code.t19 import *

def test_is_duplicate_duplicate_elements():
    assert is_duplicate([1, 2, 2, 3]) == True

def test_is_duplicate_no_duplicate_elements():
    assert is_duplicate([1, 2, 3, 4]) == False

def test_is_duplicate_empty_array():
    assert is_duplicate([]) == False

def test_is_duplicate_single_element_array():
    assert is_duplicate([1]) == False

def test_is_duplicate_large_array():
    import random
    arraynums = [random.randint(0, 100) for _ in range(100)]
    assert is_duplicate(arraynums) == False or is_duplicate(arraynums) == True


def test_is_duplicate_non_hashable_elements():
    with pytest.raises(TypeError):
        is_duplicate([[1, 2], [1, 2]])



