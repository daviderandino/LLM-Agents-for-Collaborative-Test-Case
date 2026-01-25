import pytest
from data.input_code.t9 import *


@pytest.mark.parametrize('str, tmp', [
    ('', ''),
    ('a', 'b'),
    ('ab', 'c'),
])
def test_find_Rotations_edge_cases(str, tmp):
    # The function returns the length of the string if it's not found
    assert find_Rotations(str) == len(str)

# Additional test case to cover the scenario where the string is a rotation of the concatenated string
