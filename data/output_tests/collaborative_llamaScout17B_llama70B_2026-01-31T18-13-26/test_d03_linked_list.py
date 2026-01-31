import pytest
from data.input_code.d03_linked_list import *

@pytest.fixture
def linked_list():
    return LinkedList()

def test_append_empty_list(linked_list):
    linked_list.append(5)
    assert linked_list.to_list() == [5]

def test_append_non_empty_list(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.to_list() == [5, 10]

def test_prepend_empty_list(linked_list):
    linked_list.prepend(15)
    assert linked_list.to_list() == [15]

def test_prepend_non_empty_list(linked_list):
    linked_list.append(5)
    linked_list.prepend(15)
    assert linked_list.to_list() == [15, 5]

def test_delete_head_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(5) == True
    assert linked_list.to_list() == [10]

def test_delete_middle_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(10) == True
    assert linked_list.to_list() == [5, 15]

def test_delete_tail_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.delete(15) == True
    assert linked_list.to_list() == [5, 10]

def test_delete_non_existent_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.delete(25) == False
    assert linked_list.to_list() == [5, 10]

def test_find_middle_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.find(10) == 1

def test_find_non_existent_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    assert linked_list.find(25) == -1

def test_get_middle_node(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.get(1) == 10

def test_get_index_out_of_range_negative(linked_list):
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_index_out_of_range_too_large(linked_list):
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(10)

def test_to_list(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert linked_list.to_list() == [5, 10, 15]

def test_len(linked_list):
    linked_list.append(5)
    linked_list.append(10)
    linked_list.append(15)
    assert len(linked_list) == 3