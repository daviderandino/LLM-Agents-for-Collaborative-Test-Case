import pytest
from data.input_code.t1 import min_cost


def test_min_cost_invalid_dimensions():
    with pytest.raises(TypeError):
        min_cost([[[1]]], "m", "n")







