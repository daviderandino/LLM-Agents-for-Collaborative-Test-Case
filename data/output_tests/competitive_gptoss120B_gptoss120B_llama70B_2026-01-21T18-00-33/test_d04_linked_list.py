import pytest
from data.input_code.d04_linked_list import *

def build_linked_list(values):
    """Utility to create a LinkedList pre‑populated with the given values."""
    ll = LinkedList()
    for v in values:
        ll.append(v)
    return ll

# ---------- append ----------
@pytest.mark.parametrize(
    "prepopulate, data, expected_list, expected_len",
    [
        ([], 1, [1], 1),                     # T1
        ([1], 2, [1, 2], 2),                 # T2
    ],
)
def test_append(prepopulate, data, expected_list, expected_len):
    ll = build_linked_list(prepopulate)
    ll.append(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- prepend ----------
@pytest.mark.parametrize(
    "prepopulate, data, expected_list, expected_len",
    [
        ([], 10, [10], 1),                   # T3
        ([10], 20, [20, 10], 2),             # T4
    ],
)
def test_prepend(prepopulate, data, expected_list, expected_len):
    ll = build_linked_list(prepopulate)
    ll.prepend(data)
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- delete ----------
@pytest.mark.parametrize(
    "prepopulate, data, expected_ret, expected_list, expected_len",
    [
        ([], 5, False, [], 0),                       # T5
        ([1, 2, 3], 1, True, [2, 3], 2),             # T6
        ([1, 2, 3], 2, True, [1, 3], 2),             # T7
        ([1, 2, 3], 99, False, [1, 2, 3], 3),        # T8
    ],
)
def test_delete(prepopulate, data, expected_ret, expected_list, expected_len):
    ll = build_linked_list(prepopulate)
    ret = ll.delete(data)
    assert ret is expected_ret
    assert ll.to_list() == expected_list
    assert len(ll) == expected_len

# ---------- find ----------
@pytest.mark.parametrize(
    "prepopulate, data, expected_index",
    [
        ([], 42, -1),                                 # T9
        ([1, 2, 3], 2, 1),                            # T10
        ([1, 2, 3], 99, -1),                          # T11
    ],
)
def test_find(prepopulate, data, expected_index):
    ll = build_linked_list(prepopulate)
    assert ll.find(data) == expected_index

# ---------- get ----------
@pytest.mark.parametrize(
    "prepopulate, index, expected",
    [
        ([10, 20, 30], 1, 20),                        # T12
        ([10, 20], -1, "IndexError"),                # T13
        ([10, 20], 5, "IndexError"),                 # T14
    ],
)
def test_get(prepopulate, index, expected):
    ll = build_linked_list(prepopulate)
    if expected == "IndexError":
        with pytest.raises(IndexError):
            ll.get(index)
    else:
        assert ll.get(index) == expected

# ---------- to_list ----------
@pytest.mark.parametrize(
    "prepopulate, expected_list",
    [
        ([], []),                                     # T15
        ([5, 10, 15], [5, 10, 15]),                   # T16
    ],
)
def test_to_list(prepopulate, expected_list):
    ll = build_linked_list(prepopulate)
    assert ll.to_list() == expected_list

# ---------- __len__ ----------
@pytest.mark.parametrize(
    "prepopulate, expected_len",
    [
        ([1, 2, 3, 4], 4),                            # T17
    ],
)
def test_len(prepopulate, expected_len):
    ll = build_linked_list(prepopulate)
    assert len(ll) == expected_len