import pytest
from data.input_code.d03_stack import *

# Stack tests
@pytest.mark.parametrize('item, expected', [
    (None, None),
    ("", None)
])
def test_stack_push(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.size() == 1
    assert item in stack

def test_stack_pop_nonempty():
    stack = Stack()
    stack.push("")
    assert stack.pop() == ""

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

@pytest.mark.parametrize('item, expected', [
    (None, None),
    ("", "")
])
def test_stack_peek_nonempty(item, expected):
    stack = Stack()
    stack.push(item)
    assert stack.peek() == expected

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_clear():
    stack = Stack()
    stack.push(None)
    stack.clear()
    assert stack.is_empty()

def test_stack_size():
    stack = Stack()
    stack.push(None)
    stack.push("")
    assert stack.size() == 2

def test_stack_is_empty():
    stack = Stack()
    stack.push(None)
    assert not stack.is_empty()
    stack.clear()
    assert stack.is_empty()

def test_stack_len():
    stack = Stack()
    stack.push(None)
    stack.push("")
    assert len(stack) == 2

def test_stack_contains():
    stack = Stack()
    stack.push(None)
    assert None in stack

# Queue tests
@pytest.mark.parametrize('item, expected', [
    (None, None),
    ("", None)
])
def test_queue_enqueue(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.size() == 1
    assert item in queue

def test_queue_dequeue_nonempty():
    queue = Queue()
    queue.enqueue("")
    assert queue.dequeue() == ""

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

@pytest.mark.parametrize('item, expected', [
    (None, None),
    ("", "")
])
def test_queue_front_nonempty(item, expected):
    queue = Queue()
    queue.enqueue(item)
    assert queue.front() == expected

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_clear():
    queue = Queue()
    queue.enqueue(None)
    queue.clear()
    assert queue.is_empty()

def test_queue_size():
    queue = Queue()
    queue.enqueue(None)
    queue.enqueue("")
    assert queue.size() == 2

def test_queue_is_empty():
    queue = Queue()
    queue.enqueue(None)
    assert not queue.is_empty()
    queue.clear()
    assert queue.is_empty()

def test_queue_len():
    queue = Queue()
    queue.enqueue(None)
    queue.enqueue("")
    assert len(queue) == 2

def test_queue_contains():
    queue = Queue()
    queue.enqueue(None)
    assert None in queue