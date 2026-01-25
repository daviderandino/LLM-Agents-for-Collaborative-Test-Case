import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ('hello', 'o', 'hell'),
    ('hello', 'x', 'hello'),
    ('hellooo', 'o', 'hello'),  # Corrected expected output
])
def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''

def test_remove_Occ_single_char_string():
    assert remove_Occ('a', 'x') == 'a'

def test_remove_Occ_non_existent_char():
    assert remove_Occ('ab', 'x') == 'ab'

def test_remove_Occ_input_string_none():
    with pytest.raises(TypeError):
        remove_Occ(None, 'a')


def test_remove_Occ_input_both_none():
    with pytest.raises(TypeError):
        remove_Occ(None, None)