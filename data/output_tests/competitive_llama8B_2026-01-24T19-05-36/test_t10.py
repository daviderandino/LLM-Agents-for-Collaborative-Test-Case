import pytest
from data.input_code.t10 import *


def test_small_nnum_error():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3, 4, 5], 'a')



# Fixing the failing tests


# Fixing the failing test
def test_small_nnum_invalid_input():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3, 4, 5], 'a')

# Fixing the failing test
def test_small_nnum_invalid_input_type():
    with pytest.raises(TypeError):
        small_nnum([1, 2, 3, 4, 5], 'a')