import pytest
from data.input_code.t13 import count_common


def test_count_common_empty():
    words = []
    result = count_common(words)
    assert result == []

def test_count_common_single():
    words = ['test']
    result = count_common(words)
    assert result == [('test', 1)]



def test_count_common_non_countable():
    words = [{'a': 1}, {'b': 2}, {'a': 1}]
    with pytest.raises(TypeError):
        count_common(words)

