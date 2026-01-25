import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (["apple", "banana", "cherry", "date"], [( "apple", 1), ("banana", 1), ("cherry", 1), ("date", 1)]),
    (["apple", "banana", "cherry", "date", "elderberry", "fig"], [( "apple", 1), ("banana", 1), ("cherry", 1), ("date", 1)]),
    (["apple", "banana"], [( "apple", 1), ("banana", 1)]),
    (["apple", "apple", "apple", "apple"], [( "apple", 4)]),
])
def test_count_common_success(words, expected):
    assert count_common(words) == expected

def test_count_common_empty():
    assert count_common([]) == []




def test_count_common_non_iterable():
    with pytest.raises(TypeError):
        count_common(123)

def test_count_common_non_iterable_with_none():
    with pytest.raises(TypeError):
        count_common(None, 123)

def test_count_common_non_iterable_with_string():
    with pytest.raises(TypeError):
        count_common(123, "hello")