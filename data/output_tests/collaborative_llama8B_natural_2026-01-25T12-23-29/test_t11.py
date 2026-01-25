import pytest
from data.input_code.t11 import *


def test_remove_Occ_empty_string():
    with pytest.raises(TypeError):
        remove_Occ(None, "a")




def test_remove_Occ_multiple_occurrences_from_both_ends():
    assert remove_Occ("helloo", "o") == "hell"

# Fixing the failing tests


def test_remove_Occ_multiple_occurrences_from_both_ends_correct():
    assert remove_Occ("helloo", "o") == "hell"