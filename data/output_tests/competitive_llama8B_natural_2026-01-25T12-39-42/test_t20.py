import pytest
from data.input_code.t20 import *



def test_multiples_of_num_error():
    with pytest.raises(ValueError):
        multiples_of_num(10, 0)

@pytest.mark.parametrize('m, n', [
    (10, None),
    (None, 3),
    (10, '3'),
    ('10', 3)
])
def test_multiples_of_num_error_type(m, n):
    with pytest.raises(TypeError):
        multiples_of_num(m, n)