import pytest
from data.input_code.t11 import *

def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected

@pytest.mark.parametrize('s, ch, expected', [
    ("Hello World", "o", "Hell Wrld"),
    ("Hello World", "z", "Hello World"),
    ("", "a", ""),
])
def test_remove_Occ_success_param(s, ch, expected):
    test_remove_Occ_success(s, ch, expected)

def test_remove_Occ_error_none_input():
    with pytest.raises(TypeError):
        remove_Occ(None, "a")

def test_remove_Occ_error_non_string_input():
    with pytest.raises(TypeError):
        remove_Occ(1, "a")

def test_remove_Occ_error_none_string_input():
    with pytest.raises(TypeError):
        remove_Occ(None, "a")


def test_remove_Occ_error_non_string_input_3():
    with pytest.raises(TypeError):
        remove_Occ(None, 1)


def test_remove_Occ_error_non_string_input_5():
    with pytest.raises(TypeError):
        remove_Occ(None, None)