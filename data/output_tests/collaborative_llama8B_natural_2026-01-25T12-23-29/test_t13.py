import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cherry', 'date'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
    (['apple', 'banana', 'cherry'], [('apple', 1), ('banana', 1), ('cherry', 1)]),
    (['apple', 'banana', 'cherry', 'date', 'elderberry'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
])
def test_count_common_success(words, expected):
    assert count_common(words) == expected

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_element_list():
    assert count_common(['apple']) == [('apple', 1)]

def test_count_common_duplicate_words():
    assert count_common(['apple', 'apple', 'banana', 'banana', 'cherry']) == [('apple', 2), ('banana', 2), ('cherry', 1)]





def test_count_common_non_iterable_input():
    with pytest.raises(TypeError):
        count_common(123)


def test_count_common_non_iterable_input():
    with pytest.raises(TypeError):
        count_common(123)