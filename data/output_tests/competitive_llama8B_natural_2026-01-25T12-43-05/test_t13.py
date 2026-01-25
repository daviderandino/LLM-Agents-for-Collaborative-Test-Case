import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cherry', 'date', 'elderberry'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
    (['apple', 'apple', 'banana', 'banana', 'cherry'], [('apple', 2), ('banana', 2), ('cherry', 1)]),
])
def test_count_common_success(words, expected):
    result = count_common(words)
    assert result == expected

def test_count_common_empty_list():
    result = count_common([])
    assert result == []





def test_count_common_non_iterable_input():
    with pytest.raises(TypeError):
        count_common(123)

