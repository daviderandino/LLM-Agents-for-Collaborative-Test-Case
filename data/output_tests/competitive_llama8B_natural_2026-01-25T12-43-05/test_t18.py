import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('a, expected', [
    ('Hello World', ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd'])
])
def test_str_to_list_success(a, expected):
    assert str_to_list(a) == expected

def test_str_to_list_empty_string():
    assert str_to_list('') == []

def test_str_to_list_none_input():
    with pytest.raises(TypeError):
        str_to_list(None)

@pytest.mark.parametrize('a, expected', [
    (['H', 'e', 'l', 'l', 'o'], 'Hello')
])
def test_lst_to_string_success(a, expected):
    assert lst_to_string(a) == expected

def test_lst_to_string_empty_list():
    assert lst_to_string([]) == ''

def test_lst_to_string_none_input():
    with pytest.raises(TypeError):
        lst_to_string(None)


def test_get_char_count_array_empty_string():
    assert get_char_count_array('') == [0] * 256

def test_get_char_count_array_none_input():
    with pytest.raises(TypeError):
        get_char_count_array(None)


def test_remove_dirty_chars_empty_second_string():
    assert remove_dirty_chars('Hello World', '') == 'Hello World'

def test_remove_dirty_chars_none_input():
    with pytest.raises(TypeError):
        remove_dirty_chars('Hello World', None)



