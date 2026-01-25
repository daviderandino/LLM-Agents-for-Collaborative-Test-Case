import pytest
from data.input_code.t11 import *

@pytest.mark.parametrize('s, ch, expected', [
    ('hello', 'l', 'heo'),
    ('hello', 'l', 'heo'),  # multiple occurrences
    ('hello', 'x', 'hello'),
    ('', 'a', ''),  # corrected expected value
    ('a', 'a', ''),  # corrected expected value
    ('a', 'b', 'a'),
])
def test_remove_Occ_success(s, ch, expected):
    assert remove_Occ(s, ch) == expected



