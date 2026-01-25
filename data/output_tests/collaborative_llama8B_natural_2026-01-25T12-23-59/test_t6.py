import pytest
from data.input_code.t6 import *





def test_differ_At_One_Bit_Pos_non_integer_float():
    with pytest.raises(TypeError):
        differ_At_One_Bit_Pos(4.5, 2.5)