import pytest
from data.input_code.t13 import count_common

def test_empty_list():
    words = []
    result = count_common(words)
    assert result == []

def test_single_word():
    words = ['apple']
    result = count_common(words)
    assert result == [('apple', 1)]

def test_two_distinct_words():
    words = ['apple', 'banana']
    result = count_common(words)
    assert result == [('apple', 1), ('banana', 1)]

def test_two_duplicate_words():
    words = ['apple', 'apple']
    result = count_common(words)
    assert result == [('apple', 2)]

def test_four_distinct_words():
    words = ['apple', 'banana', 'cherry', 'date']
    result = count_common(words)
    assert result == [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]

def test_four_duplicate_words():
    words = ['apple', 'apple', 'apple', 'apple']
    result = count_common(words)
    assert result == [('apple', 4)]

def test_four_words_with_one_most_common():
    words = ['apple', 'apple', 'apple', 'banana']
    result = count_common(words)
    assert result == [('apple', 3), ('banana', 1)]

def test_four_words_with_two_most_common():
    words = ['apple', 'apple', 'banana', 'banana']
    result = count_common(words)
    assert result == [('apple', 2), ('banana', 2)]

def test_four_words_with_three_most_common():
    words = ['apple', 'apple', 'apple', 'banana']
    result = count_common(words)
    assert result == [('apple', 3), ('banana', 1)]






def test_count_common_with_non_iterable():
    words = 123
    with pytest.raises(TypeError):
        count_common(words)