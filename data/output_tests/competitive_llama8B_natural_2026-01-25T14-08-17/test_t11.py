import pytest
from data.input_code.t11 import *

def test_remove_Occ_single_occurrence():
    s = 'hello'
    ch = 'l'
    expected = 'heo'
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_multiple_occurrences():
    s = 'hello'
    ch = 'l'
    expected = 'heo'
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_no_occurrences():
    s = 'hello'
    ch = 'x'
    expected = 'hello'
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_empty_string():
    s = ''
    ch = 'a'
    expected = ''
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_single_character_string():
    s = 'a'
    ch = 'a'
    expected = ''
    assert remove_Occ(s, ch) == expected


def test_remove_Occ_non_string_input():
    s = 123
    ch = 'a'
    with pytest.raises(TypeError):
        remove_Occ(s, ch)

def test_remove_Occ_none_input():
    s = None
    ch = 'a'
    with pytest.raises(TypeError):
        remove_Occ(s, ch)

def test_remove_Occ_not_in_string():
    s = 'hello'
    ch = 'k'
    expected = 'hello'
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_single_occurrence_from_right():
    s = 'hello'
    ch = 'o'
    expected = 'hell'
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_multiple_occurrences_from_right():
    s = 'hello'
    ch = 'l'
    expected = 'heo'
    assert remove_Occ(s, ch) == expected