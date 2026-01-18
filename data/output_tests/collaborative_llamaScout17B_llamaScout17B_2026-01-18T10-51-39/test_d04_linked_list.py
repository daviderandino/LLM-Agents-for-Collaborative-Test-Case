import pytest
from data.input_code.d04_linked_list import *

@pytest.mark.parametrize("data, expected", [
    (5, None),
])
def test_append_ok(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert len(linked_list) == 1
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize("data, expected", [
    (5, None),
])
def test_prepend_ok(data, expected):
    linked_list = LinkedList()
    linked_list.prepend(data)
    assert len(linked_list) == 1
    assert linked_list.to_list() == [data]

@pytest.mark.parametrize("data, expected", [
    (5, True),
])
def test_delete_ok(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 0

@pytest.mark.parametrize("data, expected", [
    (5, False),
])
def test_delete_fail(data, expected):
    linked_list = LinkedList()
    assert linked_list.delete(data) == expected

@pytest.mark.parametrize("data, expected", [
    (5, 0),
])
def test_find_ok(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("data, expected", [
    (5, -1),
])
def test_find_fail(data, expected):
    linked_list = LinkedList()
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_ok(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    assert linked_list.get(index) == expected

def test_get_err():
    linked_list = LinkedList()
    with pytest.raises(IndexError):
        linked_list.get(0)

@pytest.mark.parametrize("expected", [
    [],
])
def test_to_list_ok(expected):
    linked_list = LinkedList()
    assert linked_list.to_list() == expected

@pytest.mark.parametrize("expected", [
    0,
])
def test_len_ok(expected):
    linked_list = LinkedList()
    assert len(linked_list) == expected

@pytest.mark.parametrize("data, expected", [
    (5, True),
])
def test_delete_middle(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(data)
    linked_list.append(3)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 2
    assert linked_list.to_list() == [1, 3]

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_boundaries(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    assert linked_list.get(index) == expected

def test_get_err_large():
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(100)

def test_len_after_ops():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    assert len(linked_list) == 2

@pytest.mark.parametrize("data, expected", [
    (5, True),
])
def test_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 0

@pytest.mark.parametrize("index, expected", [
    (-1, IndexError),
])
def test_get_boundary_negative(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(expected):
        linked_list.get(index)

@pytest.mark.parametrize("data, expected", [
    (10, False),
])
def test_delete_not_found(data, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 1

def test_len_after_delete_all():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.delete(5)
    assert len(linked_list) == 0

def test_to_list_after_append():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    expected = [1, 2, 3]
    assert linked_list.to_list() == expected

@pytest.mark.parametrize("data, expected", [
    (1, True),
])
def test_delete_head_of_multiple(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 2
    assert linked_list.to_list() == [2, 3]

@pytest.mark.parametrize("data, expected", [
    (3, True),
])
def test_delete_tail(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 2
    assert linked_list.to_list() == [1, 2]

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_single_element(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize("data, expected", [
    (6, -1),
])
def test_find_not_found_in_multiple(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(3)
    assert linked_list.find(data) == expected

def test_to_list_after_prepend():
    linked_list = LinkedList()
    linked_list.prepend(1)
    linked_list.append(2)
    linked_list.append(3)
    expected = [1, 2, 3]
    assert linked_list.to_list() == expected

def test_delete_empty_list():
    linked_list = LinkedList()
    assert linked_list.delete(5) == False

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_single_element_prepend(index, expected):
    linked_list = LinkedList()
    linked_list.prepend(expected)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize("data, expected", [
    (1, 0),
])
def test_find_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(2)
    assert linked_list.find(data) == expected

@pytest.mark.parametrize("data, expected", [
    (3, 2),
])
def test_find_tail(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(data)
    assert linked_list.find(data) == expected

def test_to_list_after_delete_all():
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.delete(1)
    linked_list.delete(2)
    assert linked_list.to_list() == []

def test_delete_head_of_single():
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.delete(5) == True
    assert len(linked_list) == 0

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_last(index, expected):
    linked_list = LinkedList()
    linked_list.append(5)
    assert linked_list.get(index) == expected

@pytest.mark.parametrize("data, expected", [
    (5, 2),
])
def test_find_last(data, expected):
    linked_list = LinkedList()
    linked_list.append(1)
    linked_list.append(2)
    linked_list.append(data)
    assert linked_list.find(data) == expected

def test_prepend_multiple():
    linked_list = LinkedList()
    linked_list.prepend(5)
    linked_list.prepend(10)
    assert len(linked_list) == 2
    assert linked_list.to_list() == [10, 5]

def test_append_multiple():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(10)
    assert len(linked_list) == 2
    assert linked_list.to_list() == [5, 10]

@pytest.mark.parametrize("data, expected", [
    (5, True),
])
def test_delete_all(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list.delete(data) == expected
    assert linked_list.delete(data) == expected
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 0

def test_delete_not_found_empty():
    linked_list = LinkedList()
    assert linked_list.delete(5) == False

@pytest.mark.parametrize("data, expected", [
    (5, None),
])
def test_prepend_delete_head(data, expected):
    linked_list = LinkedList()
    linked_list.prepend(data)
    linked_list.delete(data)
    assert len(linked_list) == 0

@pytest.mark.parametrize("data, expected", [
    (5, None),
])
def test_append_delete_tail(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.delete(data)
    assert len(linked_list) == 0

def test_len_delete_all():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(5)
    linked_list.delete(5)
    linked_list.delete(5)
    assert len(linked_list) == 0

def test_to_list_delete_all():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(5)
    linked_list.delete(5)
    linked_list.delete(5)
    assert linked_list.to_list() == []

@pytest.mark.parametrize("data, expected", [
    (5, False),
])
def test_delete_not_found_head(data, expected):
    linked_list = LinkedList()
    linked_list.append(10)
    assert linked_list.delete(data) == expected
    assert len(linked_list) == 1

def test_delete_duplicates():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.append(5)
    linked_list.append(5)
    assert linked_list.delete(5) == True
    assert linked_list.to_list() == [5, 5]
    assert linked_list.delete(5) == True
    assert linked_list.to_list() == [5]
    assert linked_list.delete(5) == True
    assert linked_list.to_list() == []

@pytest.mark.parametrize("index, expected", [
    (0, 5),
])
def test_get_last_index(index, expected):
    linked_list = LinkedList()
    linked_list.append(expected)
    assert linked_list.get(index) == expected

def test_prepend_delete_head_multiple():
    linked_list = LinkedList()
    linked_list.prepend(5)
    linked_list.prepend(10)
    linked_list.delete(10)
    assert len(linked_list) == 1
    assert linked_list.to_list() == [5]

@pytest.mark.parametrize("data, expected", [
    (5, True),
])
def test_delete_duplicates_twice(data, expected):
    linked_list = LinkedList()
    linked_list.append(data)
    linked_list.append(data)
    assert linked_list.delete(data) == True
    assert linked_list.delete(data) == expected  
    assert len(linked_list) == 0  # Corrected assertion

def test_get_last_index_large_list():
    linked_list = LinkedList()
    linked_list.append(5)
    with pytest.raises(IndexError):
        linked_list.get(100)

@pytest.mark.parametrize("data, expected", [
    (5, -1),
])
def test_find_not_found_empty_list(data, expected):
    linked_list = LinkedList()
    assert linked_list.find(data) == expected

def test_prepend_delete_tail():
    linked_list = LinkedList()
    linked_list.prepend(5)
    linked_list.append(10)
    linked_list.delete(10)
    assert len(linked_list) == 1
    assert linked_list.to_list() == [5]

def test_append_delete_head_twice():
    linked_list = LinkedList()
    linked_list.append(5)
    linked_list.delete(5)
    assert len(linked_list) == 0
    assert linked_list.delete(5) == False