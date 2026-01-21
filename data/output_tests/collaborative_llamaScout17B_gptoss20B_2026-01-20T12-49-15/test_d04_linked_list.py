import pytest
from data.input_code.d04_linked_list import *

@pytest.fixture
def empty_list():
    return LinkedList()

@pytest.fixture
def list_with_two():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    return ll

# ---------- Append ----------
def test_append_ok(empty_list):
    ll = empty_list
    ll.append(5)
    assert ll.to_list() == [5]
    assert len(ll) == 1

def test_append_multiple(list_with_two):
    ll = list_with_two
    ll.append(10)
    assert ll.to_list() == [5, 10, 10]
    assert len(ll) == 3

# ---------- Prepend ----------
def test_prepend_ok(empty_list):
    ll = empty_list
    ll.prepend(5)
    assert ll.to_list() == [5]
    assert len(ll) == 1

def test_prepend_multiple(list_with_two):
    ll = list_with_two
    ll.prepend(10)
    assert ll.to_list() == [10, 5, 10]
    assert len(ll) == 3

# ---------- Delete ----------
@pytest.mark.parametrize("data,expected", [
    (5, True),   # delete head
    (10, True),  # delete tail
    (15, False), # non-existent
])
def test_delete(list_with_two, data, expected):
    ll = list_with_two
    result = ll.delete(data)
    assert result is expected
    # Verify list state after deletion
    if data == 5:
        assert ll.to_list() == [10]
    elif data == 10:
        assert ll.to_list() == [5]
    else:
        assert ll.to_list() == [5, 10]

# ---------- Find ----------
@pytest.mark.parametrize("data,expected", [
    (5, 0),   # head
    (10, 1),  # tail
    (15, -1), # non-existent
])
def test_find(list_with_two, data, expected):
    ll = list_with_two
    assert ll.find(data) == expected

# ---------- Get ----------
@pytest.mark.parametrize("index,expected", [
    (0, 5),   # head
    (1, 10),  # tail
])
def test_get_success(list_with_two, index, expected):
    ll = list_with_two
    assert ll.get(index) == expected

def test_get_out_of_range(list_with_two):
    ll = list_with_two
    with pytest.raises(IndexError):
        ll.get(2)

# ---------- to_list ----------
def test_to_list(list_with_two):
    ll = list_with_two
    assert ll.to_list() == [5, 10]

# ---------- __len__ ----------
def test_len(list_with_two):
    ll = list_with_two
    assert len(ll) == 2

import pytest
from data.input_code.d04_linked_list import *

def test_delete_from_empty(empty_list):
    ll = empty_list
    result = ll.delete(5)
    assert result is False

def test_get_negative_index(list_with_two):
    ll = list_with_two
    with pytest.raises(IndexError):
        ll.get(-1)

def test_delete_non_existent_head():
    ll = LinkedList()
    ll.append(10)
    ll.append(15)
    result = ll.delete(5)
    assert result is False

def test_delete_non_existent_tail():
    ll = LinkedList()
    ll.append(5)
    ll.append(15)
    result = ll.delete(10)
    assert result is False