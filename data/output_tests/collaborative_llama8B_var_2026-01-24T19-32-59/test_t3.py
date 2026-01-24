import pytest
from data.input_code.t3 import *


# Additional test case to handle math domain error
def test_is_not_prime_negative():
    with pytest.raises(ValueError):
        is_not_prime(-5)