import pytest
from data.input_code.t19 import is_duplicate

def test_test_duplicate_empty_list():
    assert is_duplicate([]) == False

def test_test_duplicate_single_element_list():
    assert is_duplicate([1]) == False

def test_test_duplicate_no_duplicates():
    assert is_duplicate([1, 2, 3, 4, 5]) == False

def test_test_duplicate_with_duplicates():
    assert is_duplicate([1, 2, 2, 3, 4, 4, 5]) == True

def test_test_duplicate_with_floats():
    assert is_duplicate([1.2, 2.3, 2.3, 3.4, 4.5, 4.5]) == True

def test_test_duplicate_with_strings():
    assert is_duplicate(["a", "b", "b", "c", "d", "d"]) == True

def test_test_duplicate_with_negative_numbers():
    assert is_duplicate([-1, -2, -2, -3, -4, -4]) == True

def test_test_duplicate_with_zero():
    assert is_duplicate([0, 0, 1, 2, 3, 4]) == True

def test_test_duplicate_with_none_inputs():
    with pytest.raises(TypeError):
        is_duplicate(None)


def test_test_duplicate_with_large_list():
    large_list = [i for i in range(10000)]
    large_list_set = set(large_list)
    assert is_duplicate(large_list) == (len(large_list) != len(large_list_set))