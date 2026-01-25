import pytest
from data.input_code.t13 import *
from collections import Counter


def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_word():
    assert count_common(['apple']) == [('apple', 1)]

def test_count_common_duplicate_words():
    assert count_common(['apple', 'apple', 'banana', 'banana', 'cherry']) == [('apple', 2), ('banana', 2), ('cherry', 1)]



def test_count_common_list_with_non_hashable_elements():
    with pytest.raises(TypeError):
        count_common([[1, 2], 'apple', 'banana'])


def test_count_common_list_with_non_string_and_non_hashable_elements():
    with pytest.raises(TypeError):
        count_common(['apple', [1, 2], 'banana'])

def test_count_common_success_with_top_four():
    assert len(count_common(['apple', 'banana', 'cherry', 'date', 'elderberry'])) == 4

def test_count_common_success_with_top_four_duplicate_words():
    assert len(count_common(['apple', 'apple', 'banana', 'banana', 'cherry'])) == 3