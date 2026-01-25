import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cat', 'dog', 'elephant'], [('apple', 1), ('banana', 1), ('cat', 1), ('dog', 1)]),
    (['apple', 'apple', 'apple', 'banana', 'banana'], [('apple', 3), ('banana', 2)])
])
def test_count_common_success(words, expected):
    assert count_common(words) == expected

def test_count_common_boundary():
    assert count_common(['apple', 'banana', 'cat']) == [('apple', 1), ('banana', 1), ('cat', 1)]

def test_count_common_empty_list():
    assert count_common([]) == []




def test_count_common_large_input():
    words = [str(i) for i in range(1000)]
    assert len(count_common(words)) <= 4

def test_count_common_large_input_value():
    words = [str(i) for i in range(1000)]
    result = count_common(words)
    assert isinstance(result, list)
    assert len(result) <= 4
    for item in result:
        assert isinstance(item, tuple)
        assert len(item) == 2
        assert isinstance(item[0], str)
        assert isinstance(item[1], int)