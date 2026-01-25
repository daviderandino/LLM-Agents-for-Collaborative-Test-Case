import pytest
from data.input_code.t10 import *

@pytest.mark.parametrize('list1, n, expected', [
    ([10, 20, 30, 40, 50], 3, [10, 20, 30]),
    ([-10, -20, -30, -40, -50], 3, [-50, -40, -30]),  # Corrected expected value
    ([10, -20, 30, -40, 50], 3, [-40, -20, 10]),
    ([], 3, []),
    ([10, 10, 10, 10, 10], 3, [10, 10, 10]),
    ([10, 20, 30], 10, [10, 20, 30]),
    ([10, 20, 30], 3, [10, 20, 30]),
    ([10, 20, 30], 0, []),
])
def test_small_nnum_success(list1, n, expected):
    assert small_nnum(list1, n) == expected

