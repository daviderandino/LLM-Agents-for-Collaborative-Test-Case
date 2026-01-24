import pytest
from data.input_code.t3 import is_not_prime, math




def test_is_not_prime_empty_string():
    with pytest.raises(TypeError):
        is_not_prime("")

