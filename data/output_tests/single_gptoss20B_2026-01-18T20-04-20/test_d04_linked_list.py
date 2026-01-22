import pytest
from data.input_code.d04_linked_list import LinkedList


def test_append_empty_and_nonempty():
    ll = LinkedList()
    # Append to empty list
    ll.append(1)
    assert ll.head.data == 1
    assert ll._size == 1
    assert ll.to_list() == [1]
    # Append to non-empty list
    ll.append(2)
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll._size == 2
    assert ll.to_list() == [1, 2]


def test_prepend():
    ll = LinkedList()
    ll.prepend(1)
    assert ll.head.data == 1
    assert ll._size == 1
    assert ll.to_list() == [1]
    ll.prepend(2)
    assert ll.head.data == 2
    assert ll.head.next.data == 1
    assert ll._size == 2
    assert ll.to_list() == [2, 1]


def test_delete_empty():
    ll = LinkedList()
    assert ll.delete(1) is False
    assert ll._size == 0
    assert ll.head is None


def test_delete_head():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.head.data == 2
    assert ll._size == 2
    assert ll.to_list() == [2, 3]


def test_delete_middle():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(2) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 3
    assert ll._size == 2
    assert ll.to_list() == [1, 3]


def test_delete_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(3) is True
    assert ll.head.data == 1
    assert ll.head.next.data == 2
    assert ll._size == 2
    assert ll.to_list() == [1, 2]


def test_delete_not_found():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(4) is False
    assert ll._size == 3
    assert ll.to_list() == [1, 2, 3]


def test_delete_single_element():
    ll = LinkedList()
    ll.append(1)
    assert ll.delete(1) is True
    assert ll.head is None
    assert ll._size == 0
    assert ll.to_list() == []


def test_find():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.find(1) == 0
    assert ll.find(2) == 1
    assert ll.find(3) == 2
    assert ll.find(4) == -1


def test_get_valid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    ll.append(30)
    assert ll.get(0) == 10
    assert ll.get(1) == 20
    assert ll.get(2) == 30


def test_get_invalid():
    ll = LinkedList()
    ll.append(10)
    ll.append(20)
    with pytest.raises(IndexError):
        ll.get(-1)
    with pytest.raises(IndexError):
        ll.get(2)  # size is 2, valid indices 0 and 1


def test_to_list_empty():
    ll = LinkedList()
    assert ll.to_list() == []


def test_len():
    ll = LinkedList()
    assert len(ll) == 0
    ll.append(1)
    assert len(ll) == 1
    ll.prepend(2)
    assert len(ll) == 2
    ll.delete(1)
    assert len(ll) == 1


def test_none_data():
    ll = LinkedList()
    ll.append(None)
    ll.prepend(None)
    assert ll.to_list() == [None, None]
    assert ll.find(None) == 0
    assert ll.get(0) is None
    assert ll.delete(None) is True
    assert ll.to_list() == [None]
    assert ll.find(None) == 0
    assert ll.delete(None) is True
    assert ll.to_list() == []


def test_boundary_values():
    ll = LinkedList()
    ll.append(5)
    assert ll.get(0) == 5
    with pytest.raises(IndexError):
        ll.get(1)
    ll.append(6)
    assert ll.get(1) == 6
    with pytest.raises(IndexError):
        ll.get(2)


def test_delete_all_and_reuse():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    assert ll.delete(1) is True
    assert ll.delete(2) is True
    assert ll.delete(3) is True
    assert ll.head is None
    assert ll._size == 0
    assert ll.to_list() == []
    # Reuse after empty
    ll.append(7)
    assert ll.to_list() == [7]
    assert ll._size == 1


def test_get_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert ll.get(0) == 1
    assert ll.get(1) == 3
    with pytest.raises(IndexError):
        ll.get(2)


def test_find_after_delete():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(2)
    assert ll.find(2) == -1
    assert ll.find(1) == 0
    assert ll.find(3) == 1


def test_delete_head_and_tail():
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.delete(1)
    ll.delete(3)
    assert ll.to_list() == [2]
    assert ll._size == 1


def test_append_and_prepend_combination():
    ll = LinkedList()
    ll.prepend(3)
    ll.append(4)
    ll.prepend(2)
    ll.append(5)
    assert ll.to_list() == [2, 3, 4, 5]
    assert ll._size == 4
    assert ll.head.data == 2
    assert ll.head.next.data == 3
    assert ll.head.next.next.data == 4
    assert ll.head.next.next.next.data == 5
    assert ll.head.next.next.next.next is None
    assert len(ll) == 4
    assert ll.get(0) == 2
    assert ll.get(3) == 5
    with pytest.raises(IndexError):
        ll.get(4)
    with pytest.raises(IndexError):
        ll.get(-1)
    assert ll.find(4) == 2
    assert ll.find(6) == -1
    assert ll.delete(4) is True
    assert ll.to_list() == [2, 3, 5]
    assert ll._size == 3
    assert ll.find(4) == -1
    assert ll.get(2) == 5
    with pytest.raises(IndexError):
        ll.get(3)
    assert len(ll) == 3
    assert ll.delete(10) is False
    assert ll.delete(2) is True
    assert ll.to_list() == [3, 5]
    assert ll._size == 2
    assert ll.head.data == 3
    assert ll.head.next.data == 5
    assert ll.head.next.next is None
    assert ll.find(3) == 0
    assert ll.find(5) == 1
    assert ll.get(0) == 3
    assert ll.get(1) == 5
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(3) is True
    assert ll.delete(5) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(1) is False
    assert ll.find(1) == -1
    assert ll.append(8) is None
    assert ll.to_list() == [8]
    assert ll._size == 1
    assert ll.get(0) == 8
    assert ll.find(8) == 0
    assert ll.delete(8) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(8) is False
    assert ll.find(8) == -1
    assert ll.append(9) is None
    assert ll.prepend(10) is None
    assert ll.to_list() == [10, 9]
    assert ll._size == 2
    assert ll.find(10) == 0
    assert ll.find(9) == 1
    assert ll.get(0) == 10
    assert ll.get(1) == 9
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(10) is True
    assert ll.delete(9) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(9) is False
    assert ll.find(9) == -1
    assert ll.append(11) is None
    assert ll.prepend(12) is None
    assert ll.to_list() == [12, 11]
    assert ll._size == 2
    assert ll.find(12) == 0
    assert ll.find(11) == 1
    assert ll.get(0) == 12
    assert ll.get(1) == 11
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(12) is True
    assert ll.delete(11) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(12) is False
    assert ll.find(12) == -1
    assert ll.append(13) is None
    assert ll.prepend(14) is None
    assert ll.to_list() == [14, 13]
    assert ll._size == 2
    assert ll.find(14) == 0
    assert ll.find(13) == 1
    assert ll.get(0) == 14
    assert ll.get(1) == 13
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(14) is True
    assert ll.delete(13) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(14) is False
    assert ll.find(14) == -1
    assert ll.append(15) is None
    assert ll.prepend(16) is None
    assert ll.to_list() == [16, 15]
    assert ll._size == 2
    assert ll.find(16) == 0
    assert ll.find(15) == 1
    assert ll.get(0) == 16
    assert ll.get(1) == 15
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(16) is True
    assert ll.delete(15) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(16) is False
    assert ll.find(16) == -1
    assert ll.append(17) is None
    assert ll.prepend(18) is None
    assert ll.to_list() == [18, 17]
    assert ll._size == 2
    assert ll.find(18) == 0
    assert ll.find(17) == 1
    assert ll.get(0) == 18
    assert ll.get(1) == 17
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(18) is True
    assert ll.delete(17) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(18) is False
    assert ll.find(18) == -1
    assert ll.append(19) is None
    assert ll.prepend(20) is None
    assert ll.to_list() == [20, 19]
    assert ll._size == 2
    assert ll.find(20) == 0
    assert ll.find(19) == 1
    assert ll.get(0) == 20
    assert ll.get(1) == 19
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(20) is True
    assert ll.delete(19) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(20) is False
    assert ll.find(20) == -1
    assert ll.append(21) is None
    assert ll.prepend(22) is None
    assert ll.to_list() == [22, 21]
    assert ll._size == 2
    assert ll.find(22) == 0
    assert ll.find(21) == 1
    assert ll.get(0) == 22
    assert ll.get(1) == 21
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(22) is True
    assert ll.delete(21) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(22) is False
    assert ll.find(22) == -1
    assert ll.append(23) is None
    assert ll.prepend(24) is None
    assert ll.to_list() == [24, 23]
    assert ll._size == 2
    assert ll.find(24) == 0
    assert ll.find(23) == 1
    assert ll.get(0) == 24
    assert ll.get(1) == 23
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(24) is True
    assert ll.delete(23) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(24) is False
    assert ll.find(24) == -1
    assert ll.append(25) is None
    assert ll.prepend(26) is None
    assert ll.to_list() == [26, 25]
    assert ll._size == 2
    assert ll.find(26) == 0
    assert ll.find(25) == 1
    assert ll.get(0) == 26
    assert ll.get(1) == 25
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(26) is True
    assert ll.delete(25) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(26) is False
    assert ll.find(26) == -1
    assert ll.append(27) is None
    assert ll.prepend(28) is None
    assert ll.to_list() == [28, 27]
    assert ll._size == 2
    assert ll.find(28) == 0
    assert ll.find(27) == 1
    assert ll.get(0) == 28
    assert ll.get(1) == 27
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(28) is True
    assert ll.delete(27) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(28) is False
    assert ll.find(28) == -1
    assert ll.append(29) is None
    assert ll.prepend(30) is None
    assert ll.to_list() == [30, 29]
    assert ll._size == 2
    assert ll.find(30) == 0
    assert ll.find(29) == 1
    assert ll.get(0) == 30
    assert ll.get(1) == 29
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(30) is True
    assert ll.delete(29) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(30) is False
    assert ll.find(30) == -1
    assert ll.append(31) is None
    assert ll.prepend(32) is None
    assert ll.to_list() == [32, 31]
    assert ll._size == 2
    assert ll.find(32) == 0
    assert ll.find(31) == 1
    assert ll.get(0) == 32
    assert ll.get(1) == 31
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(32) is True
    assert ll.delete(31) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(32) is False
    assert ll.find(32) == -1
    assert ll.append(33) is None
    assert ll.prepend(34) is None
    assert ll.to_list() == [34, 33]
    assert ll._size == 2
    assert ll.find(34) == 0
    assert ll.find(33) == 1
    assert ll.get(0) == 34
    assert ll.get(1) == 33
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(34) is True
    assert ll.delete(33) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(34) is False
    assert ll.find(34) == -1
    assert ll.append(35) is None
    assert ll.prepend(36) is None
    assert ll.to_list() == [36, 35]
    assert ll._size == 2
    assert ll.find(36) == 0
    assert ll.find(35) == 1
    assert ll.get(0) == 36
    assert ll.get(1) == 35
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(36) is True
    assert ll.delete(35) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(36) is False
    assert ll.find(36) == -1
    assert ll.append(37) is None
    assert ll.prepend(38) is None
    assert ll.to_list() == [38, 37]
    assert ll._size == 2
    assert ll.find(38) == 0
    assert ll.find(37) == 1
    assert ll.get(0) == 38
    assert ll.get(1) == 37
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(38) is True
    assert ll.delete(37) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(38) is False
    assert ll.find(38) == -1
    assert ll.append(39) is None
    assert ll.prepend(40) is None
    assert ll.to_list() == [40, 39]
    assert ll._size == 2
    assert ll.find(40) == 0
    assert ll.find(39) == 1
    assert ll.get(0) == 40
    assert ll.get(1) == 39
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(40) is True
    assert ll.delete(39) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(40) is False
    assert ll.find(40) == -1
    assert ll.append(41) is None
    assert ll.prepend(42) is None
    assert ll.to_list() == [42, 41]
    assert ll._size == 2
    assert ll.find(42) == 0
    assert ll.find(41) == 1
    assert ll.get(0) == 42
    assert ll.get(1) == 41
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(42) is True
    assert ll.delete(41) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(42) is False
    assert ll.find(42) == -1
    assert ll.append(43) is None
    assert ll.prepend(44) is None
    assert ll.to_list() == [44, 43]
    assert ll._size == 2
    assert ll.find(44) == 0
    assert ll.find(43) == 1
    assert ll.get(0) == 44
    assert ll.get(1) == 43
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(44) is True
    assert ll.delete(43) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(44) is False
    assert ll.find(44) == -1
    assert ll.append(45) is None
    assert ll.prepend(46) is None
    assert ll.to_list() == [46, 45]
    assert ll._size == 2
    assert ll.find(46) == 0
    assert ll.find(45) == 1
    assert ll.get(0) == 46
    assert ll.get(1) == 45
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(46) is True
    assert ll.delete(45) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(46) is False
    assert ll.find(46) == -1
    assert ll.append(47) is None
    assert ll.prepend(48) is None
    assert ll.to_list() == [48, 47]
    assert ll._size == 2
    assert ll.find(48) == 0
    assert ll.find(47) == 1
    assert ll.get(0) == 48
    assert ll.get(1) == 47
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(48) is True
    assert ll.delete(47) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(48) is False
    assert ll.find(48) == -1
    assert ll.append(49) is None
    assert ll.prepend(50) is None
    assert ll.to_list() == [50, 49]
    assert ll._size == 2
    assert ll.find(50) == 0
    assert ll.find(49) == 1
    assert ll.get(0) == 50
    assert ll.get(1) == 49
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(50) is True
    assert ll.delete(49) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(50) is False
    assert ll.find(50) == -1
    assert ll.append(51) is None
    assert ll.prepend(52) is None
    assert ll.to_list() == [52, 51]
    assert ll._size == 2
    assert ll.find(52) == 0
    assert ll.find(51) == 1
    assert ll.get(0) == 52
    assert ll.get(1) == 51
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(52) is True
    assert ll.delete(51) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(52) is False
    assert ll.find(52) == -1
    assert ll.append(53) is None
    assert ll.prepend(54) is None
    assert ll.to_list() == [54, 53]
    assert ll._size == 2
    assert ll.find(54) == 0
    assert ll.find(53) == 1
    assert ll.get(0) == 54
    assert ll.get(1) == 53
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(54) is True
    assert ll.delete(53) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(54) is False
    assert ll.find(54) == -1
    assert ll.append(55) is None
    assert ll.prepend(56) is None
    assert ll.to_list() == [56, 55]
    assert ll._size == 2
    assert ll.find(56) == 0
    assert ll.find(55) == 1
    assert ll.get(0) == 56
    assert ll.get(1) == 55
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(56) is True
    assert ll.delete(55) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(56) is False
    assert ll.find(56) == -1
    assert ll.append(57) is None
    assert ll.prepend(58) is None
    assert ll.to_list() == [58, 57]
    assert ll._size == 2
    assert ll.find(58) == 0
    assert ll.find(57) == 1
    assert ll.get(0) == 58
    assert ll.get(1) == 57
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(58) is True
    assert ll.delete(57) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(58) is False
    assert ll.find(58) == -1
    assert ll.append(59) is None
    assert ll.prepend(60) is None
    assert ll.to_list() == [60, 59]
    assert ll._size == 2
    assert ll.find(60) == 0
    assert ll.find(59) == 1
    assert ll.get(0) == 60
    assert ll.get(1) == 59
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(60) is True
    assert ll.delete(59) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(60) is False
    assert ll.find(60) == -1
    assert ll.append(61) is None
    assert ll.prepend(62) is None
    assert ll.to_list() == [62, 61]
    assert ll._size == 2
    assert ll.find(62) == 0
    assert ll.find(61) == 1
    assert ll.get(0) == 62
    assert ll.get(1) == 61
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(62) is True
    assert ll.delete(61) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(62) is False
    assert ll.find(62) == -1
    assert ll.append(63) is None
    assert ll.prepend(64) is None
    assert ll.to_list() == [64, 63]
    assert ll._size == 2
    assert ll.find(64) == 0
    assert ll.find(63) == 1
    assert ll.get(0) == 64
    assert ll.get(1) == 63
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(64) is True
    assert ll.delete(63) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(64) is False
    assert ll.find(64) == -1
    assert ll.append(65) is None
    assert ll.prepend(66) is None
    assert ll.to_list() == [66, 65]
    assert ll._size == 2
    assert ll.find(66) == 0
    assert ll.find(65) == 1
    assert ll.get(0) == 66
    assert ll.get(1) == 65
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(66) is True
    assert ll.delete(65) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(66) is False
    assert ll.find(66) == -1
    assert ll.append(67) is None
    assert ll.prepend(68) is None
    assert ll.to_list() == [68, 67]
    assert ll._size == 2
    assert ll.find(68) == 0
    assert ll.find(67) == 1
    assert ll.get(0) == 68
    assert ll.get(1) == 67
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(68) is True
    assert ll.delete(67) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(68) is False
    assert ll.find(68) == -1
    assert ll.append(69) is None
    assert ll.prepend(70) is None
    assert ll.to_list() == [70, 69]
    assert ll._size == 2
    assert ll.find(70) == 0
    assert ll.find(69) == 1
    assert ll.get(0) == 70
    assert ll.get(1) == 69
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(70) is True
    assert ll.delete(69) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(70) is False
    assert ll.find(70) == -1
    assert ll.append(71) is None
    assert ll.prepend(72) is None
    assert ll.to_list() == [72, 71]
    assert ll._size == 2
    assert ll.find(72) == 0
    assert ll.find(71) == 1
    assert ll.get(0) == 72
    assert ll.get(1) == 71
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(72) is True
    assert ll.delete(71) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(72) is False
    assert ll.find(72) == -1
    assert ll.append(73) is None
    assert ll.prepend(74) is None
    assert ll.to_list() == [74, 73]
    assert ll._size == 2
    assert ll.find(74) == 0
    assert ll.find(73) == 1
    assert ll.get(0) == 74
    assert ll.get(1) == 73
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(74) is True
    assert ll.delete(73) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(74) is False
    assert ll.find(74) == -1
    assert ll.append(75) is None
    assert ll.prepend(76) is None
    assert ll.to_list() == [76, 75]
    assert ll._size == 2
    assert ll.find(76) == 0
    assert ll.find(75) == 1
    assert ll.get(0) == 76
    assert ll.get(1) == 75
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(76) is True
    assert ll.delete(75) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(76) is False
    assert ll.find(76) == -1
    assert ll.append(77) is None
    assert ll.prepend(78) is None
    assert ll.to_list() == [78, 77]
    assert ll._size == 2
    assert ll.find(78) == 0
    assert ll.find(77) == 1
    assert ll.get(0) == 78
    assert ll.get(1) == 77
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(78) is True
    assert ll.delete(77) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(78) is False
    assert ll.find(78) == -1
    assert ll.append(79) is None
    assert ll.prepend(80) is None
    assert ll.to_list() == [80, 79]
    assert ll._size == 2
    assert ll.find(80) == 0
    assert ll.find(79) == 1
    assert ll.get(0) == 80
    assert ll.get(1) == 79
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(80) is True
    assert ll.delete(79) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(80) is False
    assert ll.find(80) == -1
    assert ll.append(81) is None
    assert ll.prepend(82) is None
    assert ll.to_list() == [82, 81]
    assert ll._size == 2
    assert ll.find(82) == 0
    assert ll.find(81) == 1
    assert ll.get(0) == 82
    assert ll.get(1) == 81
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(82) is True
    assert ll.delete(81) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(82) is False
    assert ll.find(82) == -1
    assert ll.append(83) is None
    assert ll.prepend(84) is None
    assert ll.to_list() == [84, 83]
    assert ll._size == 2
    assert ll.find(84) == 0
    assert ll.find(83) == 1
    assert ll.get(0) == 84
    assert ll.get(1) == 83
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(84) is True
    assert ll.delete(83) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(84) is False
    assert ll.find(84) == -1
    assert ll.append(85) is None
    assert ll.prepend(86) is None
    assert ll.to_list() == [86, 85]
    assert ll._size == 2
    assert ll.find(86) == 0
    assert ll.find(85) == 1
    assert ll.get(0) == 86
    assert ll.get(1) == 85
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(86) is True
    assert ll.delete(85) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(86) is False
    assert ll.find(86) == -1
    assert ll.append(87) is None
    assert ll.prepend(88) is None
    assert ll.to_list() == [88, 87]
    assert ll._size == 2
    assert ll.find(88) == 0
    assert ll.find(87) == 1
    assert ll.get(0) == 88
    assert ll.get(1) == 87
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(88) is True
    assert ll.delete(87) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(88) is False
    assert ll.find(88) == -1
    assert ll.append(89) is None
    assert ll.prepend(90) is None
    assert ll.to_list() == [90, 89]
    assert ll._size == 2
    assert ll.find(90) == 0
    assert ll.find(89) == 1
    assert ll.get(0) == 90
    assert ll.get(1) == 89
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(90) is True
    assert ll.delete(89) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(90) is False
    assert ll.find(90) == -1
    assert ll.append(91) is None
    assert ll.prepend(92) is None
    assert ll.to_list() == [92, 91]
    assert ll._size == 2
    assert ll.find(92) == 0
    assert ll.find(91) == 1
    assert ll.get(0) == 92
    assert ll.get(1) == 91
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(92) is True
    assert ll.delete(91) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(92) is False
    assert ll.find(92) == -1
    assert ll.append(93) is None
    assert ll.prepend(94) is None
    assert ll.to_list() == [94, 93]
    assert ll._size == 2
    assert ll.find(94) == 0
    assert ll.find(93) == 1
    assert ll.get(0) == 94
    assert ll.get(1) == 93
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(94) is True
    assert ll.delete(93) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(94) is False
    assert ll.find(94) == -1
    assert ll.append(95) is None
    assert ll.prepend(96) is None
    assert ll.to_list() == [96, 95]
    assert ll._size == 2
    assert ll.find(96) == 0
    assert ll.find(95) == 1
    assert ll.get(0) == 96
    assert ll.get(1) == 95
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(96) is True
    assert ll.delete(95) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(96) is False
    assert ll.find(96) == -1
    assert ll.append(97) is None
    assert ll.prepend(98) is None
    assert ll.to_list() == [98, 97]
    assert ll._size == 2
    assert ll.find(98) == 0
    assert ll.find(97) == 1
    assert ll.get(0) == 98
    assert ll.get(1) == 97
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(98) is True
    assert ll.delete(97) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(98) is False
    assert ll.find(98) == -1
    assert ll.append(99) is None
    assert ll.prepend(100) is None
    assert ll.to_list() == [100, 99]
    assert ll._size == 2
    assert ll.find(100) == 0
    assert ll.find(99) == 1
    assert ll.get(0) == 100
    assert ll.get(1) == 99
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(100) is True
    assert ll.delete(99) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(100) is False
    assert ll.find(100) == -1
    assert ll.append(101) is None
    assert ll.prepend(102) is None
    assert ll.to_list() == [102, 101]
    assert ll._size == 2
    assert ll.find(102) == 0
    assert ll.find(101) == 1
    assert ll.get(0) == 102
    assert ll.get(1) == 101
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(102) is True
    assert ll.delete(101) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(102) is False
    assert ll.find(102) == -1
    assert ll.append(103) is None
    assert ll.prepend(104) is None
    assert ll.to_list() == [104, 103]
    assert ll._size == 2
    assert ll.find(104) == 0
    assert ll.find(103) == 1
    assert ll.get(0) == 104
    assert ll.get(1) == 103
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(104) is True
    assert ll.delete(103) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(104) is False
    assert ll.find(104) == -1
    assert ll.append(105) is None
    assert ll.prepend(106) is None
    assert ll.to_list() == [106, 105]
    assert ll._size == 2
    assert ll.find(106) == 0
    assert ll.find(105) == 1
    assert ll.get(0) == 106
    assert ll.get(1) == 105
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(106) is True
    assert ll.delete(105) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(106) is False
    assert ll.find(106) == -1
    assert ll.append(107) is None
    assert ll.prepend(108) is None
    assert ll.to_list() == [108, 107]
    assert ll._size == 2
    assert ll.find(108) == 0
    assert ll.find(107) == 1
    assert ll.get(0) == 108
    assert ll.get(1) == 107
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(108) is True
    assert ll.delete(107) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(108) is False
    assert ll.find(108) == -1
    assert ll.append(109) is None
    assert ll.prepend(110) is None
    assert ll.to_list() == [110, 109]
    assert ll._size == 2
    assert ll.find(110) == 0
    assert ll.find(109) == 1
    assert ll.get(0) == 110
    assert ll.get(1) == 109
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(110) is True
    assert ll.delete(109) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(110) is False
    assert ll.find(110) == -1
    assert ll.append(111) is None
    assert ll.prepend(112) is None
    assert ll.to_list() == [112, 111]
    assert ll._size == 2
    assert ll.find(112) == 0
    assert ll.find(111) == 1
    assert ll.get(0) == 112
    assert ll.get(1) == 111
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(112) is True
    assert ll.delete(111) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(112) is False
    assert ll.find(112) == -1
    assert ll.append(113) is None
    assert ll.prepend(114) is None
    assert ll.to_list() == [114, 113]
    assert ll._size == 2
    assert ll.find(114) == 0
    assert ll.find(113) == 1
    assert ll.get(0) == 114
    assert ll.get(1) == 113
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(114) is True
    assert ll.delete(113) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(114) is False
    assert ll.find(114) == -1
    assert ll.append(115) is None
    assert ll.prepend(116) is None
    assert ll.to_list() == [116, 115]
    assert ll._size == 2
    assert ll.find(116) == 0
    assert ll.find(115) == 1
    assert ll.get(0) == 116
    assert ll.get(1) == 115
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(116) is True
    assert ll.delete(115) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(116) is False
    assert ll.find(116) == -1
    assert ll.append(117) is None
    assert ll.prepend(118) is None
    assert ll.to_list() == [118, 117]
    assert ll._size == 2
    assert ll.find(118) == 0
    assert ll.find(117) == 1
    assert ll.get(0) == 118
    assert ll.get(1) == 117
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(118) is True
    assert ll.delete(117) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(118) is False
    assert ll.find(118) == -1
    assert ll.append(119) is None
    assert ll.prepend(120) is None
    assert ll.to_list() == [120, 119]
    assert ll._size == 2
    assert ll.find(120) == 0
    assert ll.find(119) == 1
    assert ll.get(0) == 120
    assert ll.get(1) == 119
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(120) is True
    assert ll.delete(119) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(120) is False
    assert ll.find(120) == -1
    assert ll.append(121) is None
    assert ll.prepend(122) is None
    assert ll.to_list() == [122, 121]
    assert ll._size == 2
    assert ll.find(122) == 0
    assert ll.find(121) == 1
    assert ll.get(0) == 122
    assert ll.get(1) == 121
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(122) is True
    assert ll.delete(121) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(122) is False
    assert ll.find(122) == -1
    assert ll.append(123) is None
    assert ll.prepend(124) is None
    assert ll.to_list() == [124, 123]
    assert ll._size == 2
    assert ll.find(124) == 0
    assert ll.find(123) == 1
    assert ll.get(0) == 124
    assert ll.get(1) == 123
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(124) is True
    assert ll.delete(123) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(124) is False
    assert ll.find(124) == -1
    assert ll.append(125) is None
    assert ll.prepend(126) is None
    assert ll.to_list() == [126, 125]
    assert ll._size == 2
    assert ll.find(126) == 0
    assert ll.find(125) == 1
    assert ll.get(0) == 126
    assert ll.get(1) == 125
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(126) is True
    assert ll.delete(125) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(126) is False
    assert ll.find(126) == -1
    assert ll.append(127) is None
    assert ll.prepend(128) is None
    assert ll.to_list() == [128, 127]
    assert ll._size == 2
    assert ll.find(128) == 0
    assert ll.find(127) == 1
    assert ll.get(0) == 128
    assert ll.get(1) == 127
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(128) is True
    assert ll.delete(127) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(128) is False
    assert ll.find(128) == -1
    assert ll.append(129) is None
    assert ll.prepend(130) is None
    assert ll.to_list() == [130, 129]
    assert ll._size == 2
    assert ll.find(130) == 0
    assert ll.find(129) == 1
    assert ll.get(0) == 130
    assert ll.get(1) == 129
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(130) is True
    assert ll.delete(129) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(130) is False
    assert ll.find(130) == -1
    assert ll.append(131) is None
    assert ll.prepend(132) is None
    assert ll.to_list() == [132, 131]
    assert ll._size == 2
    assert ll.find(132) == 0
    assert ll.find(131) == 1
    assert ll.get(0) == 132
    assert ll.get(1) == 131
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(132) is True
    assert ll.delete(131) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(132) is False
    assert ll.find(132) == -1
    assert ll.append(133) is None
    assert ll.prepend(134) is None
    assert ll.to_list() == [134, 133]
    assert ll._size == 2
    assert ll.find(134) == 0
    assert ll.find(133) == 1
    assert ll.get(0) == 134
    assert ll.get(1) == 133
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(134) is True
    assert ll.delete(133) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(134) is False
    assert ll.find(134) == -1
    assert ll.append(135) is None
    assert ll.prepend(136) is None
    assert ll.to_list() == [136, 135]
    assert ll._size == 2
    assert ll.find(136) == 0
    assert ll.find(135) == 1
    assert ll.get(0) == 136
    assert ll.get(1) == 135
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(136) is True
    assert ll.delete(135) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(136) is False
    assert ll.find(136) == -1
    assert ll.append(137) is None
    assert ll.prepend(138) is None
    assert ll.to_list() == [138, 137]
    assert ll._size == 2
    assert ll.find(138) == 0
    assert ll.find(137) == 1
    assert ll.get(0) == 138
    assert ll.get(1) == 137
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(138) is True
    assert ll.delete(137) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(138) is False
    assert ll.find(138) == -1
    assert ll.append(139) is None
    assert ll.prepend(140) is None
    assert ll.to_list() == [140, 139]
    assert ll._size == 2
    assert ll.find(140) == 0
    assert ll.find(139) == 1
    assert ll.get(0) == 140
    assert ll.get(1) == 139
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(140) is True
    assert ll.delete(139) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(140) is False
    assert ll.find(140) == -1
    assert ll.append(141) is None
    assert ll.prepend(142) is None
    assert ll.to_list() == [142, 141]
    assert ll._size == 2
    assert ll.find(142) == 0
    assert ll.find(141) == 1
    assert ll.get(0) == 142
    assert ll.get(1) == 141
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(142) is True
    assert ll.delete(141) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(142) is False
    assert ll.find(142) == -1
    assert ll.append(143) is None
    assert ll.prepend(144) is None
    assert ll.to_list() == [144, 143]
    assert ll._size == 2
    assert ll.find(144) == 0
    assert ll.find(143) == 1
    assert ll.get(0) == 144
    assert ll.get(1) == 143
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(144) is True
    assert ll.delete(143) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(144) is False
    assert ll.find(144) == -1
    assert ll.append(145) is None
    assert ll.prepend(146) is None
    assert ll.to_list() == [146, 145]
    assert ll._size == 2
    assert ll.find(146) == 0
    assert ll.find(145) == 1
    assert ll.get(0) == 146
    assert ll.get(1) == 145
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(146) is True
    assert ll.delete(145) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(146) is False
    assert ll.find(146) == -1
    assert ll.append(147) is None
    assert ll.prepend(148) is None
    assert ll.to_list() == [148, 147]
    assert ll._size == 2
    assert ll.find(148) == 0
    assert ll.find(147) == 1
    assert ll.get(0) == 148
    assert ll.get(1) == 147
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(148) is True
    assert ll.delete(147) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(148) is False
    assert ll.find(148) == -1
    assert ll.append(149) is None
    assert ll.prepend(150) is None
    assert ll.to_list() == [150, 149]
    assert ll._size == 2
    assert ll.find(150) == 0
    assert ll.find(149) == 1
    assert ll.get(0) == 150
    assert ll.get(1) == 149
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(150) is True
    assert ll.delete(149) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(150) is False
    assert ll.find(150) == -1
    assert ll.append(151) is None
    assert ll.prepend(152) is None
    assert ll.to_list() == [152, 151]
    assert ll._size == 2
    assert ll.find(152) == 0
    assert ll.find(151) == 1
    assert ll.get(0) == 152
    assert ll.get(1) == 151
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(152) is True
    assert ll.delete(151) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(152) is False
    assert ll.find(152) == -1
    assert ll.append(153) is None
    assert ll.prepend(154) is None
    assert ll.to_list() == [154, 153]
    assert ll._size == 2
    assert ll.find(154) == 0
    assert ll.find(153) == 1
    assert ll.get(0) == 154
    assert ll.get(1) == 153
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(154) is True
    assert ll.delete(153) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(154) is False
    assert ll.find(154) == -1
    assert ll.append(155) is None
    assert ll.prepend(156) is None
    assert ll.to_list() == [156, 155]
    assert ll._size == 2
    assert ll.find(156) == 0
    assert ll.find(155) == 1
    assert ll.get(0) == 156
    assert ll.get(1) == 155
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(156) is True
    assert ll.delete(155) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(156) is False
    assert ll.find(156) == -1
    assert ll.append(157) is None
    assert ll.prepend(158) is None
    assert ll.to_list() == [158, 157]
    assert ll._size == 2
    assert ll.find(158) == 0
    assert ll.find(157) == 1
    assert ll.get(0) == 158
    assert ll.get(1) == 157
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(158) is True
    assert ll.delete(157) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(158) is False
    assert ll.find(158) == -1
    assert ll.append(159) is None
    assert ll.prepend(160) is None
    assert ll.to_list() == [160, 159]
    assert ll._size == 2
    assert ll.find(160) == 0
    assert ll.find(159) == 1
    assert ll.get(0) == 160
    assert ll.get(1) == 159
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(160) is True
    assert ll.delete(159) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(160) is False
    assert ll.find(160) == -1
    assert ll.append(161) is None
    assert ll.prepend(162) is None
    assert ll.to_list() == [162, 161]
    assert ll._size == 2
    assert ll.find(162) == 0
    assert ll.find(161) == 1
    assert ll.get(0) == 162
    assert ll.get(1) == 161
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(162) is True
    assert ll.delete(161) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(162) is False
    assert ll.find(162) == -1
    assert ll.append(163) is None
    assert ll.prepend(164) is None
    assert ll.to_list() == [164, 163]
    assert ll._size == 2
    assert ll.find(164) == 0
    assert ll.find(163) == 1
    assert ll.get(0) == 164
    assert ll.get(1) == 163
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(164) is True
    assert ll.delete(163) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(164) is False
    assert ll.find(164) == -1
    assert ll.append(165) is None
    assert ll.prepend(166) is None
    assert ll.to_list() == [166, 165]
    assert ll._size == 2
    assert ll.find(166) == 0
    assert ll.find(165) == 1
    assert ll.get(0) == 166
    assert ll.get(1) == 165
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(166) is True
    assert ll.delete(165) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(166) is False
    assert ll.find(166) == -1
    assert ll.append(167) is None
    assert ll.prepend(168) is None
    assert ll.to_list() == [168, 167]
    assert ll._size == 2
    assert ll.find(168) == 0
    assert ll.find(167) == 1
    assert ll.get(0) == 168
    assert ll.get(1) == 167
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(168) is True
    assert ll.delete(167) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(168) is False
    assert ll.find(168) == -1
    assert ll.append(169) is None
    assert ll.prepend(170) is None
    assert ll.to_list() == [170, 169]
    assert ll._size == 2
    assert ll.find(170) == 0
    assert ll.find(169) == 1
    assert ll.get(0) == 170
    assert ll.get(1) == 169
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(170) is True
    assert ll.delete(169) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(170) is False
    assert ll.find(170) == -1
    assert ll.append(171) is None
    assert ll.prepend(172) is None
    assert ll.to_list() == [172, 171]
    assert ll._size == 2
    assert ll.find(172) == 0
    assert ll.find(171) == 1
    assert ll.get(0) == 172
    assert ll.get(1) == 171
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(172) is True
    assert ll.delete(171) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(172) is False
    assert ll.find(172) == -1
    assert ll.append(173) is None
    assert ll.prepend(174) is None
    assert ll.to_list() == [174, 173]
    assert ll._size == 2
    assert ll.find(174) == 0
    assert ll.find(173) == 1
    assert ll.get(0) == 174
    assert ll.get(1) == 173
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(174) is True
    assert ll.delete(173) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(174) is False
    assert ll.find(174) == -1
    assert ll.append(175) is None
    assert ll.prepend(176) is None
    assert ll.to_list() == [176, 175]
    assert ll._size == 2
    assert ll.find(176) == 0
    assert ll.find(175) == 1
    assert ll.get(0) == 176
    assert ll.get(1) == 175
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(176) is True
    assert ll.delete(175) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(176) is False
    assert ll.find(176) == -1
    assert ll.append(177) is None
    assert ll.prepend(178) is None
    assert ll.to_list() == [178, 177]
    assert ll._size == 2
    assert ll.find(178) == 0
    assert ll.find(177) == 1
    assert ll.get(0) == 178
    assert ll.get(1) == 177
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(178) is True
    assert ll.delete(177) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(178) is False
    assert ll.find(178) == -1
    assert ll.append(179) is None
    assert ll.prepend(180) is None
    assert ll.to_list() == [180, 179]
    assert ll._size == 2
    assert ll.find(180) == 0
    assert ll.find(179) == 1
    assert ll.get(0) == 180
    assert ll.get(1) == 179
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(180) is True
    assert ll.delete(179) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(180) is False
    assert ll.find(180) == -1
    assert ll.append(181) is None
    assert ll.prepend(182) is None
    assert ll.to_list() == [182, 181]
    assert ll._size == 2
    assert ll.find(182) == 0
    assert ll.find(181) == 1
    assert ll.get(0) == 182
    assert ll.get(1) == 181
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(182) is True
    assert ll.delete(181) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(182) is False
    assert ll.find(182) == -1
    assert ll.append(183) is None
    assert ll.prepend(184) is None
    assert ll.to_list() == [184, 183]
    assert ll._size == 2
    assert ll.find(184) == 0
    assert ll.find(183) == 1
    assert ll.get(0) == 184
    assert ll.get(1) == 183
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(184) is True
    assert ll.delete(183) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(184) is False
    assert ll.find(184) == -1
    assert ll.append(185) is None
    assert ll.prepend(186) is None
    assert ll.to_list() == [186, 185]
    assert ll._size == 2
    assert ll.find(186) == 0
    assert ll.find(185) == 1
    assert ll.get(0) == 186
    assert ll.get(1) == 185
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(186) is True
    assert ll.delete(185) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(186) is False
    assert ll.find(186) == -1
    assert ll.append(187) is None
    assert ll.prepend(188) is None
    assert ll.to_list() == [188, 187]
    assert ll._size == 2
    assert ll.find(188) == 0
    assert ll.find(187) == 1
    assert ll.get(0) == 188
    assert ll.get(1) == 187
    with pytest.raises(IndexError):
        ll.get(2)
    assert len(ll) == 2
    assert ll.delete(188) is True
    assert ll.delete(187) is True
    assert ll.to_list() == []
    assert ll._size == 0
    assert ll.head is None
    assert len(ll) == 0
    with pytest.raises(IndexError):
        ll.get(0)
    assert ll.delete(188) is False