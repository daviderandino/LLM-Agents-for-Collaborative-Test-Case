import pytest
from data.input_code.t11 import *



def test_remove_Occ_zero_occurrences():
    with pytest.raises(TypeError):
        remove_Occ(None, 'a')

def test_remove_Occ_non_string_input():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')

def test_remove_Occ_empty_string():
    assert remove_Occ('', 'a') == ''



def test_remove_Occ_single_occurrence_multiple_occurrences():
    result = remove_Occ('hellooo', 'o')
    assert result.count('o') == 1

def test_remove_Occ_single_occurrence_no_occurrence():
    result = remove_Occ('hello', 'x')
    assert result.count('x') == 0

def test_remove_Occ_single_occurrence_non_string_input():
    with pytest.raises(TypeError):
        remove_Occ(123, 'a')