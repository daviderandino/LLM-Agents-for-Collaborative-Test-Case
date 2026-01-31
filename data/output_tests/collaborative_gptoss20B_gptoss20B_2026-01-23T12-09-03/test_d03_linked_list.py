import pytest
from data.input_code.d03_linked_list import *

def test_linked_list_sequence():
    ll = LinkedList()
    steps = [
        ('to_list', {}, [], False),
        ('get', {'index': 0}, 'IndexError', True),
        ('delete', {'data': 5}, False, False),
        ('find', {'data': 5}, -1, False),
        ('append', {'data': 10}, None, False),
        ('__len__', {}, 1, False),
        ('to_list', {}, [10], False),
        ('get', {'index': 0}, 10, False),
        ('find', {'data': 10}, 0, False),
        ('delete', {'data': 10}, True, False),
        ('__len__', {}, 0, False),
        ('to_list', {}, [], False),
        ('append', {'data': 1}, None, False),
        ('append', {'data': 2}, None, False),
        ('append', {'data': 3}, None, False),
        ('__len__', {}, 3, False),
        ('to_list', {}, [1, 2, 3], False),
        ('get', {'index': 2}, 3, False),
        ('get', {'index': -1}, 'IndexError', True),
        ('get', {'index': 3}, 'IndexError', True),
        ('find', {'data': 2}, 1, False),
        ('find', {'data': 4}, -1, False),
        ('delete', {'data': 2}, True, False),
        ('__len__', {}, 2, False),
        ('to_list', {}, [1, 3], False),
        ('delete', {'data': 1}, True, False),
        ('__len__', {}, 1, False),
        ('to_list', {}, [3], False),
        ('delete', {'data': 3}, True, False),
        ('__len__', {}, 0, False),
        ('to_list', {}, [], False),
        ('append', {'data': 7}, None, False),
        ('append', {'data': 8}, None, False),
        ('delete', {'data': 9}, False, False),
        ('prepend', {'data': ''}, None, False),
        ('to_list', {}, ['', 7, 8], False),
        ('prepend', {'data': None}, None, False),
        ('to_list', {}, [None, '', 7, 8], False),
        ('find', {'data': None}, 0, False),
        ('delete', {'data': None}, True, False),
        ('to_list', {}, ['', 7, 8], False),
        ('delete', {'data': ''}, True, False),
        ('to_list', {}, [7, 8], False),
    ]

    for step, (method, args, expected, is_exc) in enumerate(steps, start=1):
        if method == 'append':
            ll.append(args['data'])
        elif method == 'prepend':
            ll.prepend(args['data'])
        elif method == 'delete':
            result = ll.delete(args['data'])
            assert result == expected, f"Step {step}: delete({args['data']}) expected {expected} got {result}"
        elif method == 'find':
            result = ll.find(args['data'])
            assert result == expected, f"Step {step}: find({args['data']}) expected {expected} got {result}"
        elif method == 'get':
            if is_exc:
                with pytest.raises(IndexError):
                    ll.get(args['index'])
            else:
                result = ll.get(args['index'])
                assert result == expected, f"Step {step}: get({args['index']}) expected {expected} got {result}"
        elif method == 'to_list':
            result = ll.to_list()
            assert result == expected, f"Step {step}: to_list expected {expected} got {result}"
        elif method == '__len__':
            result = len(ll)
            assert result == expected, f"Step {step}: len(ll) expected {expected} got {result}"
        else:
            raise ValueError(f"Unknown method {method}")