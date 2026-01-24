import pytest
from data.input_code.t16 import text_lowercase_underscore




def test_text_lowercase_underscore_none():
    # Given
    pattern = '^[a-z]+_[a-z]+$'
    text = None
    with pytest.raises(TypeError):
        text_lowercase_underscore(text)