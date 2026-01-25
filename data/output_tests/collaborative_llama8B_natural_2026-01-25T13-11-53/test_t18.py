import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('string, expected', [
    ("Hello", ['H', 'e', 'l', 'l', 'o']),
    ("", []),
    (None, [])
])
def test_str_to_list(string, expected):
    if string is None:
        with pytest.raises(TypeError):
            str_to_list(string)
    else:
        assert str_to_list(string) == expected

@pytest.mark.parametrize('List, expected', [
    (['a', 'b', 'c'], 'abc'),
    (['a', 'b', 'c', 'd'], 'abcd'),
    ([''], ''),
    (None, '')
])
def test_lst_to_string(List, expected):
    if List is None:
        with pytest.raises(TypeError):
            lst_to_string(List)
    else:
        assert lst_to_string(List) == expected


@pytest.mark.parametrize('string, second_string, expected', [
    ("Hello", "aeiou", "Hll"),
    ("", "aeiou", ""),
    ("Hello", "", "Hello"),
    ("Hello", "aeiou", "Hll"),
    ("Hello", None, pytest.raises(TypeError)),
    ("áéíóú", "áéíóú", ""),
    ("áéíóú", "áéíóú", "")
])
def test_remove_dirty_chars(string, second_string, expected):
    if second_string is None:
        with pytest.raises(TypeError):
            remove_dirty_chars(string, second_string)
    else:
        assert remove_dirty_chars(string, second_string) == expected

