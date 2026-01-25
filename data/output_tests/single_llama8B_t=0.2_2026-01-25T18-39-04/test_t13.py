import pytest
from data.input_code.t13 import count_common

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_element():
    assert count_common(["hello"]) == [("hello", 1)]

def test_count_common_four_elements():
    assert count_common(["hello", "world", "hello", "world"]) == [("hello", 2), ("world", 2)]

def test_count_common_more_than_four_elements():
    assert count_common(["hello", "world", "hello", "world", "foo", "bar"]) == [("hello", 2), ("world", 2), ("foo", 1), ("bar", 1)]

def test_count_common_no_duplicates():
    assert count_common(["hello", "world", "foo", "bar"]) == [("hello", 1), ("world", 1), ("foo", 1), ("bar", 1)]

def test_count_common_empty_string():
    assert count_common([""]) == [("", 1)]



