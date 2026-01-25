import pytest
from data.input_code.t13 import count_common

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_element():
    assert count_common(["apple"]) == [("apple", 1)]

def test_count_common_four_elements():
    assert count_common(["apple", "banana", "apple", "orange"]) == [("apple", 2), ("banana", 1), ("orange", 1)]

def test_count_common_more_than_four_elements():
    assert count_common(["apple", "banana", "apple", "orange", "banana", "banana"]) == [("banana", 3), ("apple", 2), ("orange", 1)]




def test_count_common_non_list_input():
    with pytest.raises(TypeError):
        count_common(123)

