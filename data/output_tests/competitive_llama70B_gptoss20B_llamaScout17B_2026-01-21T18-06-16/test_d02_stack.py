import pytest
from data.input_code.d02_stack import *

# Helper to map exception names to actual exception classes
EXCEPTIONS = {
    'IndexError': IndexError,
    'ZeroDivisionError': ZeroDivisionError,
}

# Test cases for Stack
stack_test_cases = [
    {'target': 'Stack.__init__', 'input': {}, 'expected': None},
    {'target': 'Stack.push', 'input': {'item': 1}, 'expected': None},
    {'target': 'Stack.pop', 'input': {}, 'expected': 1, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.pop', 'input': {}, 'expected': 'IndexError'},
    {'target': 'Stack.peek', 'input': {}, 'expected': 1, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.peek', 'input': {}, 'expected': 'IndexError'},
    {'target': 'Stack.is_empty', 'input': {}, 'expected': False, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.is_empty', 'input': {}, 'expected': True},
    {'target': 'Stack.size', 'input': {}, 'expected': 1, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.size', 'input': {}, 'expected': 0},
    {'target': 'Stack.clear', 'input': {}, 'expected': None, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.__len__', 'input': {}, 'expected': 1, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.__len__', 'input': {}, 'expected': 0},
    {'target': 'Stack.__contains__', 'input': {'item': 1}, 'expected': True, 'setup': {'push': {'item': 1}}},
    {'target': 'Stack.__contains__', 'input': {'item': 1}, 'expected': False},
]

# Test cases for Queue
queue_test_cases = [
    {'target': 'Queue.__init__', 'input': {}, 'expected': None},
    {'target': 'Queue.enqueue', 'input': {'item': 1}, 'expected': None},
    {'target': 'Queue.dequeue', 'input': {}, 'expected': 1, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.dequeue', 'input': {}, 'expected': 'IndexError'},
    {'target': 'Queue.front', 'input': {}, 'expected': 1, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.front', 'input': {}, 'expected': 'IndexError'},
    {'target': 'Queue.is_empty', 'input': {}, 'expected': False, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.is_empty', 'input': {}, 'expected': True},
    {'target': 'Queue.size', 'input': {}, 'expected': 1, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.size', 'input': {}, 'expected': 0},
    {'target': 'Queue.clear', 'input': {}, 'expected': None, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.__len__', 'input': {}, 'expected': 1, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.__len__', 'input': {}, 'expected': 0},
    {'target': 'Queue.__contains__', 'input': {'item': 1}, 'expected': True, 'setup': {'enqueue': {'item': 1}}},
    {'target': 'Queue.__contains__', 'input': {'item': 1}, 'expected': False},
]

def _run_test_case(case):
    """Utility to execute a single test case."""
    cls_name, method_name = case['target'].split('.')
    # Instantiate the appropriate class
    if cls_name == 'Stack':
        obj = Stack()
    elif cls_name == 'Queue':
        obj = Queue()
    else:
        raise ValueError(f"Unknown class {cls_name}")

    # Perform any required setup
    if 'setup' in case:
        for setup_method, args in case['setup'].items():
            getattr(obj, setup_method)(**args)

    # Handle __init__ specially: already instantiated
    if method_name == '__init__':
        assert obj is not None
        return

    # Retrieve the method to test
    method = getattr(obj, method_name)

    # Determine expected outcome
    expected = case['expected']

    # If an exception is expected
    if isinstance(expected, str) and expected in EXCEPTIONS:
        with pytest.raises(EXCEPTIONS[expected]):
            method(**case['input'])
    else:
        result = method(**case['input'])
        assert result == expected

@pytest.mark.parametrize('case', stack_test_cases)
def test_stack(case):
    _run_test_case(case)

@pytest.mark.parametrize('case', queue_test_cases)
def test_queue(case):
    _run_test_case(case)