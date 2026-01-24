import pytest
from data.input_code.t4 import *

@pytest.mark.parametrize('nums, n, expected', [
    ([1, 2, 3, 4, 5], 3, [5, 4, 3]),
    ([1, 2, 3, 4, 5], 6, "ValueError"),
    ([1, 2, 3, 4, 5], 0, "ValueError"),
    ([], 3, []),
    ([1], 3, [1])
])
def test_heap_queue_largest(nums, n, expected):
    try:
        result = heap_queue_largest(nums, n)
        if isinstance(expected, str):
            pytest.raises(ValueError)
        else:
            assert result == expected
    except ValueError as e:
        if isinstance(expected, str) and expected == "ValueError":
            assert str(e) == "ValueError"
        else:
            pytest.fail(f"Unexpected error: {str(e)}")