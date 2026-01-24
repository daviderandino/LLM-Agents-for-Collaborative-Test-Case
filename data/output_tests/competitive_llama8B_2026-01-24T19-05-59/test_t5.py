import pytest
from data.input_code.t5 import *


def test_count_ways_error():
    with pytest.raises(TypeError):
        count_ways('a')