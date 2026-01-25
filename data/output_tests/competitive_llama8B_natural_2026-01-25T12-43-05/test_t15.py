import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_input():
    result = split_lowerstring('')
    assert result == []

def test_split_lowerstring_no_matches():
    result = split_lowerstring('ABC123')
    assert result == []
    result = split_lowerstring('!!!!!!')
    assert result == []
    result = split_lowerstring('   ')
    assert result == []


