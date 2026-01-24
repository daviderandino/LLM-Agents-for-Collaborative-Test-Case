import pytest
from data.input_code.t13 import count_common

class TestCountCommon:
    def create_test_data(self, words):
        return words

    
    
    def test_count_common_empty_list(self):
        # Test case with empty list
        words = []
        expected_result = []
        assert count_common(words) == expected_result
    
    def test_count_common_single_word(self):
        # Test case with single word
        words = ["apple"]
        expected_result = [('apple', 1)]
        assert count_common(words) == expected_result
    
    def test_count_common_duplicates(self):
        # Test case with duplicates
        words = ["apple", "apple", "apple"]
        expected_result = [('apple', 3)]
        assert count_common(words) == expected_result
    
