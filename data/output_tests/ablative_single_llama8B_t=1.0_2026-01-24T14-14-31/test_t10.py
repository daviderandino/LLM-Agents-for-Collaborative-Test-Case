import pytest
from data.input_code.t10 import small_nnum, heapq

def test_small_nnum_success():
  # Test case for success scenarios
  list1 = [5, 2, 8, 1, 9]
  n = 3
  result = small_nnum(list1, n)
  assert result == [1, 2, 5]



def test_small_nnum_invalid_input_type():
  # Test case for invalid input types
  list1 = [1, 2, 3]
  n = "string"  # or any other invalid type
  with pytest.raises(TypeError):
    small_nnum(list1, n)



def test_small_nnum_none():
  # Test case for a None input
  list1 = None
  n = 3
  with pytest.raises(TypeError):
    small_nnum(list1, n)