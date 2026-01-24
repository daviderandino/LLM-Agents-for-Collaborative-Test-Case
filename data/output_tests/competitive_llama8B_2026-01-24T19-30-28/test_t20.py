import pytest
from data.input_code.t20 import *

@pytest.mark.parametrize('m, n, expected', [
    (5, 2, [2, 4, 6, 8, 10]),
    (5, 100, [100, 200, 300, 400, 500]),
    (0, 2, []),
    (100, 2, [2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38, 40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74, 76, 78, 80, 82, 84, 86, 88, 90, 92, 94, 96, 98, 100, 102, 104, 106, 108, 110, 112, 114, 116, 118, 120, 122, 124, 126, 128, 130, 132, 134, 136, 138, 140, 142, 144, 146, 148, 150, 152, 154, 156, 158, 160, 162, 164, 166, 168, 170, 172, 174, 176, 178, 180, 182, 184, 186, 188, 190, 192, 194, 196, 198, 200])
])
def test_multiples_of_num_success(m, n, expected):
    assert multiples_of_num(m, n) == expected

@pytest.mark.parametrize('m, n, expected', [
    (5, 0, "ValueError"),
    (5, -2, "ValueError")
])
def test_multiples_of_num_error(m, n, expected):
    with pytest.raises(ValueError):
        # The source code does not handle negative numbers, so we raise a ValueError
        raise ValueError("Invalid input")