import pytest
from data.input_code.t11 import remove_Occ

def test_remove_Occ_success_string():
    # Given
    given_string = "Hello World"
    char_to_remove = "o"
    
    # When
    actual_result = remove_Occ(given_string, char_to_remove)
    
    # Then
    assert actual_result == "Hell Wrld"

def test_remove_Occ_remove_min_string():
    # Given
    given_string = "a"
    char_to_remove = "a"
    
    # When
    actual_result = remove_Occ(given_string, char_to_remove)
    
    # Then
    assert actual_result == ""

def test_remove_Occ_no_occurrences():
    # Given
    given_string = ""
    char_to_remove = "a"
    
    # When
    actual_result = remove_Occ(given_string, char_to_remove)
    
    # Then
    assert actual_result == ""

def test_remove_Occ_not_existing_character():
    # Given
    given_string = "Hello World"
    char_to_remove = "!"
    
    # When
    actual_result = remove_Occ(given_string, char_to_remove)
    
    # Then
    assert actual_result == "Hello World"

def test_remove_Occ_input_type_string():
    # Given
    given_string = "Hello, World!"
    char_to_remove = "o"
    
    # When
    with pytest.raises(TypeError):
        remove_Occ(given_string)