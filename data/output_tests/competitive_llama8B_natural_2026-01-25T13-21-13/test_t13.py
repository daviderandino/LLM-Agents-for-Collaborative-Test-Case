import pytest
from data.input_code.t13 import *

def test_count_common_happy_path():
    words = ['apple', 'banana', 'cherry', 'date']
    expected = [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]
    assert count_common(words) == expected

def test_count_common_repeated_word():
    words = ['apple', 'banana', 'cherry', 'apple']
    expected = [('apple', 2), ('banana', 1), ('cherry', 1)]
    assert count_common(words) == expected

def test_count_common_extra_word():
    words = ['apple', 'banana', 'cherry', 'date', 'elderberry']
    expected = [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]
    assert count_common(words) == expected

def test_count_common_empty_list():
    words = []
    expected = []
    assert count_common(words) == expected

def test_count_common_duplicate_words():
    words = ['banana', 'banana', 'banana', 'banana']
    expected = [('banana', 4)]
    assert count_common(words) == expected

def test_count_common_single_word():
    words = ['banana']
    expected = [('banana', 1)]
    assert count_common(words) == expected

def test_count_common_zero_count():
    words = ['banana', 'cherry']
    expected = [('banana', 1), ('cherry', 1)]
    assert count_common(words) == expected



def test_count_common_large_input():
    words = ['banana'] * 1000 + ['cherry'] * 500 + ['apple'] * 200 + ['date'] * 100
    expected = [('banana', 1000), ('cherry', 500), ('apple', 200), ('date', 100)]
    assert count_common(words) == expected

def test_count_common_none_in_list():
    words = ['banana', None, 'cherry']
    expected = [('banana', 1), (None, 1), ('cherry', 1)]
    assert count_common(words) == expected

