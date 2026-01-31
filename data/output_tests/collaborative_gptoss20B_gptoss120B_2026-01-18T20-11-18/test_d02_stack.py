import pytest
from data.input_code.d02_stack import *

def test_stack_operations():
    stack = Stack()
    # Push and verify size, length, and containment
    stack.push('x')
    assert stack.size() == 1
    assert len(stack) == 1
    assert 'x' in stack

    # Pop the element and verify it is returned
    assert stack.pop() == 'x'
    assert stack.is_empty()

    # Pop from empty stack should raise IndexError
    with pytest.raises(IndexError):
        stack.pop()

    # Peek from empty stack should raise IndexError
    with pytest.raises(IndexError):
        stack.peek()

    # Clear an empty stack (no effect)
    stack.clear()
    assert stack.size() == 0

    # Push again, then clear and verify emptiness
    stack.push('x')
    stack.clear()
    assert stack.size() == 0
    assert 'y' not in stack

def test_queue_operations():
    queue = Queue()
    # Enqueue and verify size, length, and containment
    queue.enqueue(10)
    assert queue.size() == 1
    assert len(queue) == 1
    assert 10 in queue

    # Dequeue the element and verify it is returned
    assert queue.dequeue() == 10
    assert queue.is_empty()

    # Dequeue from empty queue should raise IndexError
    with pytest.raises(IndexError):
        queue.dequeue()

    # Front from empty queue should raise IndexError
    with pytest.raises(IndexError):
        queue.front()

    # Clear an empty queue (no effect)
    queue.clear()
    assert queue.size() == 0

    # Enqueue again, then clear and verify emptiness
    queue.enqueue(10)
    queue.clear()
    assert queue.size() == 0
    assert 99 not in queue

import pytest
from data.input_code.d02_stack import *

def test_stack_peek_nonempty():
    stack = Stack()
    for item in ["alpha"]:
        stack.push(item)
    assert stack.peek() == "alpha"

def test_stack_multiple_push_pop():
    stack = Stack()
    for item in ["first", "second", "third"]:
        stack.push(item)
    assert stack.pop() == "third"

def test_stack_size_after_pop():
    stack = Stack()
    for item in ["one", "two"]:
        stack.push(item)
    stack.pop()
    assert stack.size() == 1

def test_queue_front_nonempty():
    queue = Queue()
    queue.enqueue(42)
    assert queue.front() == 42

def test_queue_multiple_enq_deq():
    queue = Queue()
    for item in ["a", "b", "c"]:
        queue.enqueue(item)
    assert queue.dequeue() == "a"

def test_queue_size_after_dequeue():
    queue = Queue()
    for item in [1, 2, 3]:
        queue.enqueue(item)
    queue.dequeue()
    assert queue.size() == 2