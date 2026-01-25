import pytest
from data.input_code.t15 import *


def test_split_lowerstring_empty_string():
    assert split_lowerstring('') == []



# The correct regular expression should be '[a-z]+[^a-z]*'
# This will match one or more lowercase letters followed by any characters.
import re
def split_lowerstring_corrected(text):
    return (re.findall('[a-z]+[^a-z]*', text))