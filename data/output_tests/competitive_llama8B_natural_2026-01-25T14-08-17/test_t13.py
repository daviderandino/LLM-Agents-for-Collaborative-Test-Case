import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cherry', 'date'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
    (['apple', 'banana', 'cherry'], [('apple', 1), ('banana', 1), ('cherry', 1)]),
    (['apple', 'apple', 'apple', 'apple'], [('apple', 4),]),
])
def test_count_common_success(words, expected):
    result = count_common(words)
    assert result == expected

def test_count_common_empty_list():
    result = count_common([])
    assert result == []


def test_count_common_large_input():
    words = [str(i) for i in range(10000)]
    result = count_common(words)
    assert len(result) == 4
    for item in result:
        assert item[1] > 0

def test_count_common_repeated_words():
    words = ['apple', 'apple', 'apple', 'banana', 'banana']
    result = count_common(words)
    expected = Counter(words).most_common(4)
    assert result == expected