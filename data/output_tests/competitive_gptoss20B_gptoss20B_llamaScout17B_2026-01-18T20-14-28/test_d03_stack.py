import pytest
from data.input_code.d03_stack import *

def test_stack_pop_non_empty():
    stack = Stack()
    stack.push(42)
    assert stack.pop() == 42

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_non_empty():
    stack = Stack()
    stack.push("x")
    assert stack.peek() == "x"

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_stack_is_empty_true():
    stack = Stack()
    assert stack.is_empty() is True

def test_stack_is_empty_false():
    stack = Stack()
    stack.push(1)
    assert stack.is_empty() is False

def test_stack_size_after_pushes():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert stack.size() == 2

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    result = stack.clear()
    assert result is None
    assert stack.is_empty() is True

def test_stack_len_after_pushes():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    assert len(stack) == 2

def test_stack_contains_true():
    stack = Stack()
    stack.push(5)
    assert 5 in stack

def test_stack_contains_false():
    stack = Stack()
    stack.push(5)
    assert 6 not in stack

def test_queue_dequeue_non_empty():
    queue = Queue()
    queue.enqueue("a")
    assert queue.dequeue() == "a"

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_non_empty():
    queue = Queue()
    queue.enqueue("b")
    assert queue.front() == "b"

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()

def test_queue_is_empty_true():
    queue = Queue()
    assert queue.is_empty() is True

def test_queue_is_empty_false():
    queue = Queue()
    queue.enqueue(1)
    assert queue.is_empty() is False

def test_queue_size_after_enqueues():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert queue.size() == 2

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    result = queue.clear()
    assert result is None
    assert queue.is_empty() is True

def test_queue_len_after_enqueues():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    assert len(queue) == 2

def test_queue_contains_true():
    queue = Queue()
    queue.enqueue(3)
    assert 3 in queue

def test_queue_contains_false():
    queue = Queue()
    queue.enqueue(3)
    assert 4 not in queue