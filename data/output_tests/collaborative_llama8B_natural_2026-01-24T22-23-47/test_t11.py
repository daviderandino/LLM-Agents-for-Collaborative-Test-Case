import pytest
from data.input_code.t11 import *

def test_remove_Occ(s, ch, expected):
    if s is None or not isinstance(s, str):
        with pytest.raises(TypeError):
            remove_Occ(s, ch)
    else:
        assert remove_Occ(s, ch) == expected

@pytest.mark.parametrize('s, ch, expected', [
    ('hello', 'l', 'heo'),
    ('hello', 'x', 'hello'),
    ('hello', 'l', 'heo'),
    ('', 'a', ''),
    ('a', 'a', ''),
    ('a', 'b', 'a'),
    ('hello', None, 'hello'),
    ('hello', 123, 'hello')
])
def test_remove_Occ(s, ch, expected):
    if s is None or not isinstance(s, str):
        with pytest.raises(TypeError):
            remove_Occ(s, ch)
    else:
        assert remove_Occ(s, ch) == expected

def test_remove_Occ_no_occurrence():
    assert remove_Occ('hello', 'o') == 'hell'

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''

def test_remove_Occ_single_char_string():
    assert remove_Occ('a', 'a') == ''

def test_remove_Occ_none_input_string():
    with pytest.raises(TypeError):
        remove_Occ(None, 'a')


def test_remove_Occ_non_string_input_string():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')


def test_remove_Occ_single_occurrence():
    assert remove_Occ('hello', 'l') == 'heo'

def test_remove_Occ_multiple_occurrences():
    assert remove_Occ('hello', 'l') == 'heo'

def test_remove_Occ_remove_from_both_sides():
    assert remove_Occ('hello', 'l') == 'heo'