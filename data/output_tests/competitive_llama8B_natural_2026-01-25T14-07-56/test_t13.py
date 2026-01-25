import pytest
from data.input_code.t13 import *
from collections import Counter


@pytest.mark.parametrize('words, expected', [
    (['apple'], [('apple', 1)]),
    (['apple', 'banana', 'cherry', 'date', 'elderberry', 'fig', 'grape', 'honeydew', 'ice cream', 'jackfruit', 'kiwi', 'lemon', 'mango', 'nectarine', 'orange', 'pineapple', 'quince', 'raspberry', 'strawberry', 'tangerine', 'ugli fruit', 'victoria plum', 'watermelon', 'xigua', 'yellow passionfruit', 'zucchini'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
    (['apple', 'apple', 'banana', 'banana', 'cherry', 'date'], [('apple', 2), ('banana', 2), ('cherry', 1), ('date', 1)]),
])
def test_count_common_large_input(words, expected):
    result = count_common(words)
    assert result == expected