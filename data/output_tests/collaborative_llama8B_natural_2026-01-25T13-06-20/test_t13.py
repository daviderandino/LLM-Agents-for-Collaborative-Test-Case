import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cat', 'dog', 'elephant'], [('apple', 1), ('banana', 1), ('cat', 1), ('dog', 1)]),
    (['apple', 'apple', 'apple', 'banana', 'banana'], [('apple', 3), ('banana', 2)]),
    (['apple', 'apple', 'apple', 'apple', 'apple'], [('apple', 5)]),
    (['apple'], [('apple', 1)]),
    (['apple', 'banana'], [('apple', 1), ('banana', 1)]),
    (['apple'] * 20 + ['banana'] * 10, [('apple', 20), ('banana', 10)]),
    (['apple'] + ['banana'] * 10000, [('banana', 10000), ('apple', 1)]),
])
def test_count_common_success(words, expected):
    assert count_common(words) == expected

def test_count_common_empty_list():
    assert count_common([]) == []

