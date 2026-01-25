import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ('hello', 'l', 'heo'),
    ('hello', 'k', 'hello'),
    ('', 'a', ''),
    ('a', 'a', ''),
    ('hello', 'l', 'heo'),
    ('llama', 'l', 'ama'),
])
def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''

def test_remove_Occ_single_character_string():
    assert remove_Occ('a', 'a') == ''

def test_remove_Occ_none_input():
    with pytest.raises(TypeError):
        remove_Occ(None, 'a')

def test_remove_Occ_non_string_input():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')