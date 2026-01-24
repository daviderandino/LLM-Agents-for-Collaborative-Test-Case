import pytest
from data.input_code.t11 import remove_Occ


def test_remove_Occ_min_length():
    s = 'a'
    ch = 'a'
    expected = ''
    assert remove_Occ(s, ch) == expected


def test_remove_Occ_none_string():
    s = None
    ch = 'a'
    with pytest.raises(TypeError):
        remove_Occ(s, ch)


def test_remove_Occ_not_found():
    s = 'Hello, World!'
    ch = '!'
    expected = 'Hello, World'
    assert remove_Occ(s, ch) == expected



def test_remove_Occ_string_empty():
    s = ''
    ch = 'a'
    expected = ''
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_string_only_ch():
    s = 'a'
    ch = 'a'
    expected = ''
    assert remove_Occ(s, ch) == expected