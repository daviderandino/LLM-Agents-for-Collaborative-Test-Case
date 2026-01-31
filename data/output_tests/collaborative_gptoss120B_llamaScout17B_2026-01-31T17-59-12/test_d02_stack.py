import pytest
from data.input_code.d02_stack import *

# Stack tests

@pytest.mark.parametrize('item', [None, 'test', 123])
def test_stack_push(item):
    stack = Stack()
    stack.push(item)
    assert len(stack) == 1
    assert item in stack

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('item', ['test', 123, None])
def test_stack_pop_success(item):
    stack = Stack()
    stack.push(item)
    assert stack.pop() == item
    assert stack.is_empty()

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('item', ['test', 123, None])
def test_stack_peek_success(item):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == item
    assert len(stack) == 1

def test_stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty()

@pytest.mark.parametrize('items', [[0], [None], ['test']])
def test_stack_is_empty_false(items):
    stack = Stack()
    for item in items:
        stack.push(item)
    assert not stack.is_empty()

@pytest.mark.parametrize('items', [[1, 2, 3], ['a', 'b', 'c']])
def test_stack_size(items):
    stack = Stack()
    for item in items:
        stack.push(item)
    assert stack.size() == len(items)

def test_stack_clear():
    stack = Stack()
    stack.push('test')
    stack.clear()
    assert stack.is_empty()

@pytest.mark.parametrize('items', [[5, 6], ['a', 'b']])
def test_stack_len(items):
    stack = Stack()
    for item in items:
        stack.push(item)
    assert len(stack) == len(items)

@pytest.mark.parametrize('item, contains', [('item', True), (123, False)])
def test_stack_contains(item, contains):
    stack = Stack()
    stack.push('item')
    assert (item in stack) == contains

# Queue tests

@pytest.mark.parametrize('item', [None, 'test', 123])
def test_queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert len(queue) == 1
    assert item in queue

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('item', ['test', 123, None])
def test_queue_dequeue_success(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.dequeue() == item
    assert queue.is_empty()

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('item', ['test', 123, None])
def test_queue_front_success(item):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == item
    assert len(queue) == 1

def test_queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty()

@pytest.mark.parametrize('items', [[None], ['test']])
def test_queue_is_empty_false(items):
    queue = Queue()
    for item in items:
        queue.enqueue(item)
    assert not queue.is_empty()

@pytest.mark.parametrize('items', [[1, 2, 3, 4], ['a', 'b', 'c']])
def test_queue_size(items):
    queue = Queue()
    for item in items:
        queue.enqueue(item)
    assert queue.size() == len(items)

def test_queue_clear():
    queue = Queue()
    queue.enqueue('test')
    queue.clear()
    assert queue.is_empty()

@pytest.mark.parametrize('items', [['a', 'b'], [5, 6]])
def test_queue_len(items):
    queue = Queue()
    for item in items:
        queue.enqueue(item)
    assert len(queue) == len(items)

@pytest.mark.parametrize('item, contains', [('elem', True), (0, False)])
def test_queue_contains(item, contains):
    queue = Queue()
    queue.enqueue('elem')
    assert (item in queue) == contains