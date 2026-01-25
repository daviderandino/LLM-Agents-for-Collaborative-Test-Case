import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ('hello', 'l', 'heo'),
    ('hello', 'x', 'hello'),
    ('', 'a', ''),
    ('a', 'a', ''),
    ('helloo', 'o', 'hell'),
    ('hello', 'h', 'ello'),
    ('hello', 'o', 'hell'),
    ('hello', 'l', 'heo'),
    ('helloo', 'o', 'hell'),
])
def test_remove_Occ(s, ch, expected):
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''

def test_remove_Occ_single_character_string():
    assert remove_Occ('a', 'a') == ''

def test_remove_Occ_multiple_occurrences():
    assert remove_Occ('helloo', 'o') == 'hell'

def test_remove_Occ_character_at_start():
    assert remove_Occ('hello', 'h') == 'ello'

def test_remove_Occ_character_at_end():
    assert remove_Occ('hello', 'o') == 'hell'

def test_remove_Occ_character_in_middle():
    assert remove_Occ('hello', 'l') == 'heo'

def test_remove_Occ_character_at_start_and_end():
    assert remove_Occ('helloo', 'o') == 'hell'