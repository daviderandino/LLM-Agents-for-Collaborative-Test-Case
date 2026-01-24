import pytest
from data.input_code.t13 import count_common

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_word():
    assert count_common(["apple"]) == [("apple", 1)]

def test_count_common_four_distinct_words():
    assert count_common(["apple", "banana", "cherry", "date"]) == [("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1)]

def test_count_common_four_distinct_words_with_duplicates():
    assert count_common(["apple", "apple", "banana", "banana"]) == [("apple", 2), ("banana", 2)]



def test_count_common_more_than_four_distinct_words():
    assert count_common(["apple", "banana", "cherry", "date", "elderberry", "fig"]) == [("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1)]


