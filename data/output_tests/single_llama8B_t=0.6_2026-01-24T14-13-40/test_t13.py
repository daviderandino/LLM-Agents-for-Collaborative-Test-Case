import pytest
from data.input_code.t13 import count_common


def test_count_common_empty_list():
    # Test with an empty list
    words = []
    expected_result = []
    assert count_common(words) == expected_result

def test_count_common_single_word():
    # Test with a list containing a single word
    words = ["hello"]
    expected_result = [("hello", 1)]
    assert count_common(words) == expected_result

def test_count_common_no_duplicates():
    # Test with a list containing no duplicates
    words = ["apple", "banana", "orange"]
    expected_result = [("apple", 1), ("banana", 1), ("orange", 1)]
    assert count_common(words) == expected_result



