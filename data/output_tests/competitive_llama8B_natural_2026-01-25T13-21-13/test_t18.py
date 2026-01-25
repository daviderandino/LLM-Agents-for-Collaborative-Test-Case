import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('input, expected', [
    ('hello', ['h', 'e', 'l', 'l', 'o'])
])
def test_str_to_list_success(input, expected):
    assert str_to_list(input) == expected

def test_str_to_list_empty():
    assert str_to_list('') == []

def test_str_to_list_single_char():
    assert str_to_list('a') == ['a']

@pytest.mark.parametrize('input, expected', [
    ('hello', 'hello')
])
def test_lst_to_string_success(input, expected):
    assert lst_to_string(input) == expected

def test_lst_to_string_empty():
    assert lst_to_string([]) == ''

def test_get_char_count_array_normal():
    expected = [0] * NO_OF_CHARS
    expected[ord('h')] = 1
    expected[ord('e')] = 1
    expected[ord('l')] = 2
    expected[ord('o')] = 1
    assert get_char_count_array('hello') == expected

def test_get_char_count_array_single_char():
    expected = [0] * NO_OF_CHARS
    expected[ord('a')] = 1
    assert get_char_count_array('a') == expected

def test_get_char_count_array_empty():
    assert get_char_count_array('') == [0] * NO_OF_CHARS

@pytest.mark.parametrize('input, second_string, expected', [
    ('hello', 'l', 'heo')
])
def test_remove_dirty_chars_success(input, second_string, expected):
    assert remove_dirty_chars(input, second_string) == expected

def test_remove_dirty_chars_empty():
    assert remove_dirty_chars('', 'l') == ''

def test_remove_dirty_chars_single_char():
    assert remove_dirty_chars('a', 'l') == 'a'


def test_remove_dirty_chars_no_dirty_chars():
    assert remove_dirty_chars('hello', 'x') == 'hello'

def test_remove_dirty_chars_non_existent_char():
    assert remove_dirty_chars('hello', 'a') == 'hello'

def test_remove_dirty_chars_non_ascii_char():
    with pytest.raises(IndexError):
        remove_dirty_chars('hello', '€')

def test_remove_dirty_chars_invalid_input():
    with pytest.raises(TypeError):
        remove_dirty_chars(123, 'l')