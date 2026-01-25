import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('string, expected', [
    ('Hello', ['H', 'e', 'l', 'l', 'o'])
])
def test_str_to_list_success(string, expected):
    assert str_to_list(string) == expected

def test_str_to_list_empty_string():
    assert str_to_list('') == []

def test_str_to_list_none_input():
    with pytest.raises(TypeError):
        str_to_list(None)

@pytest.mark.parametrize('List, expected', [
    ('Hello', 'Hello')
])
def test_lst_to_string_success(List, expected):
    assert lst_to_string(List) == expected

def test_lst_to_string_empty_list():
    assert lst_to_string([]) == ''

def test_lst_to_string_none_input():
    with pytest.raises(TypeError):
        lst_to_string(None)


def test_get_char_count_array_empty_string():
    assert get_char_count_array('') == [0]*256

def test_get_char_count_array_none_input():
    with pytest.raises(TypeError):
        get_char_count_array(None)


def test_remove_dirty_chars_dirty_character_absence():
    assert remove_dirty_chars('abc', 'Helo') == 'abc'

def test_remove_dirty_chars_empty_string():
    assert remove_dirty_chars('', 'abc') == ''

def test_remove_dirty_chars_none_input():
    with pytest.raises(TypeError):
        remove_dirty_chars(None, 'abc')

def test_remove_dirty_chars_dirty_character_presence():
    assert remove_dirty_chars('abc', 'abc') == ''

def test_remove_dirty_chars_dirty_character_absence():
    assert remove_dirty_chars('abc', 'Helo') == 'abc'