import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'apple', 'orange', 'banana', 'banana'], "[('banana', 3), ('apple', 2), ('orange', 1)]"),
    (['apple'], "[('apple', 1)]"),
    (['apple', 'banana', 'apple', 'orange'], "[('apple', 2), ('banana', 1), ('orange', 1)]"),
])
def test_count_common_success(words, expected):
    result = count_common(words)
    # Convert the result to a list of tuples and then to a string for comparison
    result_str = str(result).replace(' ', '')
    expected_str = str(eval(expected)).replace(' ', '')
    assert result_str == expected_str

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_empty_string():
    assert count_common(['']) == [('']]

def test_count_common_none_in_list():
    assert count_common([None]) == [(None, 1)]

def test_count_common_none_and_other_elements():
    assert count_common(['apple', None, 'apple']) == [('apple', 2), (None, 1)]

def test_count_common_single_element():
    assert count_common(['apple', 'apple']) == [('apple', 2)]

def test_count_common_multiple_elements():
    assert count_common(['apple', 'banana', 'apple', 'orange', 'banana', 'banana']) == [('banana', 3), ('apple', 2), ('orange', 1)]

def test_count_common_duplicates():
    assert count_common(['apple', 'apple', 'apple', 'banana', 'banana', 'banana']) == [('apple', 3), ('banana', 3)]

def test_count_common_no_duplicates():
    assert count_common(['apple', 'banana', 'orange']) == [('apple', 1), ('banana', 1), ('orange', 1)]

def test_count_common_none_in_list_with_duplicates():
    assert count_common(['apple', None, 'apple', None, 'apple']) == [('apple', 3), (None, 2)]