import pytest
from data.input_code.03_linked_list import *

@pytest.mark.parametrize("data", [5])
def test_init(data):
    ll = LinkedList()
    assert ll.head is None
    assert len(ll) == 0

@pytest.mark.parametrize("data", [5])
def test_append_empty(data):
    ll = LinkedList()
    ll.append(data)
    assert ll.head.data == data
    assert ll.head.next is None
    assert len(ll) == 1

@pytest.mark.parametrize("first, second", [(5, 10)])
def test_append_non_empty(first, second):
    ll = LinkedList()
    ll.append(first)
    ll.append(second)
    assert ll.head.data == first
    assert ll.head.next.data == second
    assert ll.head.next.next is None
    assert len(ll) == 2

@pytest.mark.parametrize("data", [5])
def test_prepend_empty(data):
    ll = LinkedList()
    ll.prepend(data)
    assert ll.head.data == data
    assert ll.head.next is None
    assert len(ll) == 1

@pytest.mark.parametrize("first, second", [(5, 10)])
def test_prepend_non_empty(first, second):
    ll = LinkedList()
    ll.prepend(first)
    ll.prepend(second)
    assert ll.head.data == second
    assert ll.head.next.data == first
    assert ll.head.next.next is None
    assert len(ll) == 2

@pytest.mark.parametrize("data", [5])
def test_delete_head(data):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    result = ll.delete(data)
    assert result is True
    assert ll.head.data == 10
    assert ll.head.next is None
    assert len(ll) == 1

@pytest.mark.parametrize("data", [10])
def test_delete_tail(data):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    result = ll.delete(data)
    assert result is True
    assert ll.head.data == 5
    assert ll.head.next is None
    assert len(ll) == 1

@pytest.mark.parametrize("data", [15])
def test_delete_non_existent(data):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    result = ll.delete(data)
    assert result is False
    assert ll.to_list() == [5, 10]
    assert len(ll) == 2

@pytest.mark.parametrize("data, expected_index", [(5, 0), (10, 1)])
def test_find(data, expected_index):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert ll.find(data) == expected_index

def test_find_non_existent():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert ll.find(15) == -1

@pytest.mark.parametrize("index, expected_value", [(0, 5), (1, 10)])
def test_get(index, expected_value):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert ll.get(index) == expected_value

def test_get_out_of_range():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    with pytest.raises(IndexError):
        ll.get(2)

def test_to_list():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert ll.to_list() == [5, 10]

def test_len():
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    assert len(ll) == 2

import pytest
from data.input_code.03_linked_list import LinkedList

def test_delete_empty_list():
    ll = LinkedList()
    result = ll.delete(5)
    assert result is False
    assert len(ll) == 0

@pytest.mark.parametrize("index", [-1])
def test_get_negative_index(index):
    ll = LinkedList()
    ll.append(5)
    ll.append(10)
    with pytest.raises(IndexError):
        ll.get(index)

@pytest.mark.parametrize("data", [5])
def test_delete_middle_node(data):
    ll = LinkedList()
    ll.append(10)
    ll.append(5)
    ll.append(15)
    result = ll.delete(data)
    assert result is True
    assert ll.to_list() == [10, 15]
    assert len(ll) == 2