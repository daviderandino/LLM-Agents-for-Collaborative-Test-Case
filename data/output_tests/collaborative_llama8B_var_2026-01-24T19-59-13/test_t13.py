import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'apple', 'orange', 'banana', 'banana'], [('banana', 3), ('apple', 2), ('orange', 1)]),
    ([], []),
    ([''], [('', 1)]),
    (['', ''], [('', 2)]),
    (['apple', 'banana', 'apple', 'orange', 'banana', 'banana', 'banana'], [('banana', 4), ('apple', 2), ('orange', 1)])
])
def test_count_common(words, expected):
    result = count_common(words)
    for item in expected:
        assert item in result