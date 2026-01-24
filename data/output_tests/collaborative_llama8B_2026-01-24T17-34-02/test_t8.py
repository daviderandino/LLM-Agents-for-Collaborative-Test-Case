import pytest
from data.input_code.t8 import *

@pytest.mark.parametrize('input_data, expected', [
    ({"nums": [1, 2, 3, 4, 5]}, [1, 4, 9, 16, 25]),
    ({"nums": []}, []),
    ({"nums": [0]}, [0]),
    ({"nums": [-1, 0, 1]}, [1, 0, 1])
])
def test_square_nums_success(input_data, expected):
    assert square_nums(input_data.get("nums", [])) == expected

def test_square_nums_error():
    with pytest.raises(TypeError):
        square_nums(None)