import pytest
from data.input_code.03_linked_list import LinkedList, Node

@pytest.fixture
def linked_list():
    return LinkedList()

def test_append_empty(linked_list):
    linked_list.append(1)
    assert linked_list.head.data == 1
    assert len(linked_list) == 1

def test_append_nonempty(linked_list):
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 2
    assert len(linked_list) == 2

def test_prepend_empty(linked_list):
    linked_list.prepend(10)
    assert linked_list.head.data == 10
    assert len(linked_list) == 1

def test_prepend_nonempty(linked_list):
    linked_list.prepend(10)
    linked_list.prepend(20)
    assert linked_list.head.data == 20
    assert linked_list.head.next.data == 10
    assert len(linked_list) == 2

def test_delete_empty(linked_list):
    assert linked_list.delete(99) == False

def test_delete_head(linked_list):
    linked_list.append(1)
    assert linked_list.delete(1) == True
    assert linked_list.head is None

def test_delete_middle(linked_list):
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(2) == True
    assert linked_list.head.data == 1
    assert linked_list.head.next.data == 3

def test_delete_not_found(linked_list):
    linked_list.append(1)
    linked_list.append(2)
    assert linked_list.delete(999) == False

def test_find_empty(linked_list):
    assert linked_list.find(5) == -1

def test_find_head(linked_list):
    linked_list.append(10)
    assert linked_list.find(10) == 0

def test_find_middle(linked_list):
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert linked_list.find(20) == 1

def test_get_valid_zero(linked_list):
    linked_list.append(10)
    assert linked_list.get(0) == 10

def test_get_valid_last(linked_list):
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert linked_list.get(2) == 30

def test_get_negative(linked_list):
    linked_list.append(10)
    with pytest.raises(IndexError):
        linked_list.get(-1)

def test_get_out_of_range(linked_list):
    linked_list.append(10)
    with pytest.raises(IndexError):
        linked_list.get(1)

def test_to_list_empty(linked_list):
    assert linked_list.to_list() == []

def test_to_list_populated(linked_list):
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert linked_list.to_list() == [10, 20, 30]

def test_len_after_operations(linked_list):
    linked_list.append(10)
    linked_list.append(20)
    linked_list.append(30)
    assert len(linked_list) == 3