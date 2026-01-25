import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (["apple", "banana", "cherry", "date"], [("apple", 1), ("banana", 1), ("cherry", 1), ("date", 1)]),
    (["apple", "banana", "banana", "cherry"], [("banana", 2), ("apple", 1), ("cherry", 1)]),  # Removed 'date' from expected
    (["apple", "banana"], [("apple", 1), ("banana", 1)]),
    (["apple", "apple", "apple"], [("apple", 3)]),
])
def test_count_common_success(words, expected):
    result = count_common(words)
    assert result == expected



