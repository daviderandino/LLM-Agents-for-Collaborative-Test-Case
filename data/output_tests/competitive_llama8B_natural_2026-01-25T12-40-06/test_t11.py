import pytest
from data.input_code.t11 import *


def test_remove_Occ_single_char():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')

def test_remove_Occ_non_string():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')

def test_remove_Occ_multiple_occurrences():
    assert remove_Occ('helloo', 'o') == 'hell'

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''

def test_remove_Occ_single_occurrence():
    assert remove_Occ('hello', 'l') == 'heo'