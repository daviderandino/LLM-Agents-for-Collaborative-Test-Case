import pytest
from data.input_code.d03_linked_list import *

def _run_operations(operations):
    """Execute a list of operations on a LinkedList and return a list of results."""
    ll = LinkedList()
    results = []
    for op in operations:
        method_name = op["method"]
        args = op.get("args", [])
        if method_name == "append":
            ll.append(*args)
        elif method_name == "prepend":
            ll.prepend(*args)
        elif method_name == "delete":
            results.append(ll.delete(*args))
        elif method_name == "find":
            results.append(ll.find(*args))
        elif method_name == "get":
            try:
                results.append(ll.get(*args))
            except IndexError:
                results.append("IndexError")
        elif method_name == "to_list":
            results.append(ll.to_list())
        elif method_name == "__len__":
            results.append(len(ll))
        else:
            raise ValueError(f"Unknown method {method_name}")
    return ll, results

def test_append():
    operations = [
        {"method": "append", "args": [1]},
        {"method": "append", "args": [2]}
    ]
    ll, _ = _run_operations(operations)
    assert len(ll) == 2
    assert ll.to_list() == [1, 2]

def test_prepend():
    operations = [
        {"method": "prepend", "args": [3]},
        {"method": "prepend", "args": [4]}
    ]
    ll, _ = _run_operations(operations)
    assert len(ll) == 2
    assert ll.to_list() == [4, 3]

def test_delete():
    operations = [
        {"method": "delete", "args": [1]},
        {"method": "append", "args": [5]},
        {"method": "append", "args": [6]},
        {"method": "append", "args": [7]},
        {"method": "delete", "args": [5]},
        {"method": "delete", "args": [6]},
        {"method": "delete", "args": [8]}
    ]
    ll, results = _run_operations(operations)
    assert results == [False, True, True, False]
    assert len(ll) == 1
    assert ll.to_list() == [7]

def test_find():
    operations = [
        {"method": "find", "args": [9]},
        {"method": "append", "args": [9]},
        {"method": "append", "args": [10]},
        {"method": "append", "args": [11]},
        {"method": "find", "args": [9]},
        {"method": "find", "args": [10]},
        {"method": "find", "args": [12]}
    ]
    _, results = _run_operations(operations)
    assert results == [-1, 0, 1, -1]

def test_get():
    operations = [
        {"method": "get", "args": [0]},
        {"method": "append", "args": [20]},
        {"method": "append", "args": [30]},
        {"method": "get", "args": [0]},
        {"method": "get", "args": [1]},
        {"method": "get", "args": [-1]},
        {"method": "get", "args": [2]}
    ]
    _, results = _run_operations(operations)
    assert results == ["IndexError", 20, 30, "IndexError", "IndexError"]

def test_to_list():
    operations = [
        {"method": "to_list", "args": []},
        {"method": "append", "args": [40]},
        {"method": "append", "args": [50]},
        {"method": "to_list", "args": []}
    ]
    _, results = _run_operations(operations)
    assert results == [[], [40, 50]]

def test_len():
    operations = [
        {"method": "__len__", "args": []},
        {"method": "append", "args": [60]},
        {"method": "__len__", "args": []},
        {"method": "prepend", "args": [70]},
        {"method": "__len__", "args": []},
        {"method": "delete", "args": [60]},
        {"method": "__len__", "args": []}
    ]
    _, results = _run_operations(operations)
    # Filter out boolean results from delete operations
    len_results = [r for r in results if not isinstance(r, bool)]
    assert len_results == [0, 1, 2, 1]

def test_missing_full_coverage():
    operations = [
        {"method": "append", "args": [1]},
        {"method": "append", "args": [2]},
        {"method": "append", "args": [3]},
        {"method": "delete", "args": [3]},
        {"method": "to_list", "args": []},
        {"method": "delete", "args": [2]},
        {"method": "to_list", "args": []},
        {"method": "delete", "args": [1]},
        {"method": "to_list", "args": []},
        {"method": "append", "args": [4]},
        {"method": "append", "args": [5]},
        {"method": "append", "args": [6]},
        {"method": "find", "args": [6]},
        {"method": "find", "args": [4]},
        {"method": "find", "args": [5]},
        {"method": "append", "args": [7]},
        {"method": "append", "args": [8]},
        {"method": "append", "args": [7]},
        {"method": "delete", "args": [7]},
        {"method": "to_list", "args": []},
        {"method": "find", "args": [7]},
        {"method": "get", "args": [2]},
        {"method": "__len__", "args": []}
    ]
    _, results = _run_operations(operations)
    expected = [True, [1, 2], True, [1], True, [], 2, 0, 1, True, [4, 5, 6, 8, 7], 4, 6, 5]
    assert results == expected