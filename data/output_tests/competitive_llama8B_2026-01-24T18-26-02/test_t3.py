import pytest
from data.input_code.t3 import *


# Additional test to check for ValueError
def test_is_not_prime_value_error():
    with pytest.raises(ValueError):
        is_not_prime(-5)