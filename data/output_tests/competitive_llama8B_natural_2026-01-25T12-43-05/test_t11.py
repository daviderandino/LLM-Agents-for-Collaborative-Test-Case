import pytest
from data.input_code.t11 import *


def test_remove_Occ_error():
    with pytest.raises(TypeError):
        remove_Occ(None, 'a')



def test_remove_Occ_non_alphabetical():
    assert remove_Occ('hello123', 'o') == 'hell123'