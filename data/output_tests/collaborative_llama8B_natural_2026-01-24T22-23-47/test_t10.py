import pytest
from data.input_code.t10 import *


@pytest.mark.parametrize('list1, n', [
    ([10, 5, 3, 8, 2], 2.5),
    ([10, 'a', 3, 8, 2], 2),
    ([10, [3, 4], 8, 2], 2)
])
def test_small_nnum_type_error(list1, n):
    with pytest.raises(TypeError):
        small_nnum(list1, n)