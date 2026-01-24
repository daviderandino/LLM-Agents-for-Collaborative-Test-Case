import pytest
from data.input_code.t18 import *

@pytest.mark.parametrize('string, expected', [
    ("Hello", ['H', 'e', 'l', 'l', 'o']),
    ("", []),
    ("Hello, World!", ['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!'])
])
def test_str_to_list(string, expected):
    assert str_to_list(string) == expected

@pytest.mark.parametrize('List, expected', [
    (['H', 'e', 'l', 'l', 'o'], "Hello"),
    ([], ""),
    (['H', 'e', 'l', 'l', 'o', ',', ' ', 'W', 'o', 'r', 'l', 'd', '!'], "Hello, World!")
])
def test_lst_to_string(List, expected):
    assert lst_to_string(List) == expected








