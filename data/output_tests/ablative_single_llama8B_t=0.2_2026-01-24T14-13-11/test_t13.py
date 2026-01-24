import pytest
from data.input_code.t13 import count_common

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_word():
    assert count_common(["hello"]) == [("hello", 1)]

def test_count_common_four_unique_words():
    assert count_common(["hello", "world", "python", "test"]) == [("hello", 1), ("world", 1), ("python", 1), ("test", 1)]

def test_count_common_four_unique_words_with_duplicates():
    assert count_common(["hello", "hello", "world", "world"]) == [("hello", 2), ("world", 2)]

def test_count_common_four_unique_words_with_duplicates_and_third_most_common():
    assert count_common(["hello", "hello", "hello", "world", "world"]) == [("hello", 3), ("world", 2)]

def test_count_common_four_unique_words_with_duplicates_and_third_most_common_and_fourth_most_common():
    assert count_common(["hello", "hello", "hello", "hello", "world", "world"]) == [("hello", 4), ("world", 2)]

def test_count_common_more_than_four_unique_words():
    assert count_common(["hello", "world", "python", "test", "foo", "bar"]) == [("hello", 1), ("world", 1), ("python", 1), ("test", 1)]

def test_count_common_more_than_four_unique_words_with_duplicates():
    assert count_common(["hello", "hello", "world", "world", "python", "python", "test", "test"]) == [("hello", 2), ("world", 2), ("python", 2), ("test", 2)]


