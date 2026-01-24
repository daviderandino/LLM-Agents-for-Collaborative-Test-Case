import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'apple', 'orange', 'banana', 'banana'], [('banana', 3), ('apple', 2), ('orange', 1)]),
    ([], []),
    ([''], [('', 1)]),
    (['a'] * 1000, [('a', 1000)]),
    (['a', 'b', 'c'], [('a', 1), ('b', 1), ('c', 1)]),
])
def test_count_common(words, expected):
    result = count_common(words)
    assert result == expected