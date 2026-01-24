import pytest
from data.input_code.t15 import *


@pytest.mark.parametrize('text', [
    None,
    123,
])
def test_split_lowerstring_type_error(text):
    with pytest.raises(TypeError):
        split_lowerstring(text)


# Additional test case to cover the logic of split_lowerstring

# Additional test case to cover the logic of split_lowerstring

# Additional test case to cover the logic of split_lowerstring

# Additional test case to cover the logic of split_lowerstring

# Additional test case to cover the logic of split_lowerstring
def test_split_lowerstring_with_multiple_consecutive_uppercase():
    assert split_lowerstring('HELLOHELLOHELLO') == []