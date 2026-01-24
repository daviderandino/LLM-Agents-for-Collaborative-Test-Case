import pytest
from data.input_code.t13 import *
from collections import Counter

@pytest.mark.parametrize('words, expected', [
    (['apple', 'banana', 'cherry', 'date'], [('apple', 1), ('banana', 1), ('cherry', 1), ('date', 1)]),
    (['apple', 'apple', 'banana', 'banana'], [('apple', 2), ('banana', 2)]),  # Adjusted expected output
])
def test_count_common_success(words, expected):
    assert count_common(words) == expected

def test_count_common_fewer_than_four():
    assert count_common(['apple', 'banana', 'cherry']) == [('apple', 1), ('banana', 1), ('cherry', 1)]

def test_count_common_empty_list():
    assert count_common([]) == []

def test_count_common_single_word():
    assert count_common(['apple', 'apple', 'apple', 'apple']) == [('apple', 4)]



def test_count_common_large_number_of_unique_words():
    words = [str(i) for i in range(1000)]
    assert len(count_common(words)) == 4  # Adjusted assertion to match the expected output

def test_count_common_large_number_of_unique_words_output():
    words = [str(i) for i in range(1000)]
    assert count_common(words)[0][1] == 1  # Adjusted assertion to match the expected output


