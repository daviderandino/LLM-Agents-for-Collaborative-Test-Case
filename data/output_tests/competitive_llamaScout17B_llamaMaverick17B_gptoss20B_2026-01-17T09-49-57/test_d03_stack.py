import pytest
from data.input_code.d03_stack import *

# Test Stack
@pytest.mark.parametrize('expected', [None])
def test_stack_init(expected):
    stack = Stack()
    assert stack.is_empty() == True

def test_stack_push():
    stack = Stack()
    stack.push(5)
    assert stack.peek() == 5

def test_stack_pop():
    stack = Stack()
    stack.push(5)
    assert stack.pop() == 5

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek():
    stack = Stack()
    stack.push(5)
    assert stack.peek() == 5

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

@pytest.mark.parametrize('expected', [True, False])
def test_stack_is_empty(expected):
    stack = Stack()
    if not expected:
        stack.push(5)
    assert stack.is_empty() == expected

def test_stack_size():
    stack = Stack()
    stack.push(5)
    assert stack.size() == 1

def test_stack_clear():
    stack = Stack()
    stack.push(5)
    stack.clear()
    assert stack.is_empty() == True

def test_stack_len():
    stack = Stack()
    stack.push(5)
    assert len(stack) == 1

@pytest.mark.parametrize('item, expected', [(5, True), (10, False)])
def test_stack_contains(item, expected):
    stack = Stack()
    stack.push(5)
    assert (item in stack) == expected

# Test Queue
@pytest.mark.parametrize('expected', [None])
def test_queue_init(expected):
    queue = Queue()
    assert queue.is_empty() == True

def test_queue_enqueue():
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == 5

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(5)
    assert queue.dequeue() == 5

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front():
    queue = Queue()
    queue.enqueue(5)
    assert queue.front() == 5

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

@pytest.mark.parametrize('expected', [True, False])
def test_queue_is_empty(expected):
    queue = Queue()
    if not expected:
        queue.enqueue(5)
    assert queue.is_empty() == expected

def test_queue_size():
    queue = Queue()
    queue.enqueue(5)
    assert queue.size() == 1

def test_queue_clear():
    queue = Queue()
    queue.enqueue(5)
    queue.clear()
    assert queue.is_empty() == True

def test_queue_len():
    queue = Queue()
    queue.enqueue(5)
    assert len(queue) == 1

@pytest.mark.parametrize('item, expected', [(5, True), (10, False)])
def test_queue_contains(item, expected):
    queue = Queue()
    queue.enqueue(5)
    assert (item in queue) == expected