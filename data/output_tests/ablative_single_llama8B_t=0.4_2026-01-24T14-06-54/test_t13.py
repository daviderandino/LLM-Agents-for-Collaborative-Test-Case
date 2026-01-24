import pytest
from data.input_code.t13 import count_common

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_element():
    assert count_common(['apple']) == [('apple', 1)]

def test_count_common_four_elements():
    assert count_common(['apple', 'banana', 'cherry', 'date']) == [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]

def test_count_common_more_than_four_elements():
    assert count_common(['apple', 'banana', 'cherry', 'date', 'elderberry']) == [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]

def test_count_common_duplicates():
    assert count_common(['apple', 'apple', 'banana', 'banana', 'cherry']) == [('apple', 2), ('banana', 2), ('cherry', 1)]

def test_count_common_empty_string():
    assert count_common('') == []

def test_count_common_none_input():
    assert count_common(None) == []


def test_count_common_non_string_input():
    with pytest.raises(TypeError):
        count_common(123)