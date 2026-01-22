import pytest
from data.input_code.d03_stack import *

def test_stack_init():
    stack = Stack()
    assert stack.is_empty() == True

@pytest.mark.parametrize("item", [1, "a", 3.14])
def test_stack_push(item):
    stack = Stack()
    stack.push(item)
    assert item in stack

def test_stack_pop():
    stack = Stack()
    stack.push(1)
    assert stack.pop() == 1

def test_stack_peek():
    stack = Stack()
    stack.push(1)
    assert stack.peek() == 1

def test_stack_is_empty():
    stack = Stack()
    assert stack.is_empty() == True
    stack.push(1)
    assert stack.is_empty() == False

def test_stack_size():
    stack = Stack()
    assert stack.size() == 0
    stack.push(1)
    assert stack.size() == 1

def test_stack_clear():
    stack = Stack()
    stack.push(1)
    stack.clear()
    assert stack.is_empty() == True

def test_stack_len():
    stack = Stack()
    assert len(stack) == 0
    stack.push(1)
    assert len(stack) == 1

def test_stack_contains():
    stack = Stack()
    stack.push(1)
    assert 1 in stack

def test_stack_pop_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()

def test_stack_peek_empty():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.peek()

def test_queue_init():
    queue = Queue()
    assert queue.is_empty() == True

@pytest.mark.parametrize("item", [1, "a", 3.14])
def test_queue_enqueue(item):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

def test_queue_dequeue():
    queue = Queue()
    queue.enqueue(1)
    assert queue.dequeue() == 1

def test_queue_front():
    queue = Queue()
    queue.enqueue(1)
    assert queue.front() == 1

def test_queue_is_empty():
    queue = Queue()
    assert queue.is_empty() == True
    queue.enqueue(1)
    assert queue.is_empty() == False

def test_queue_size():
    queue = Queue()
    assert queue.size() == 0
    queue.enqueue(1)
    assert queue.size() == 1

def test_queue_clear():
    queue = Queue()
    queue.enqueue(1)
    queue.clear()
    assert queue.is_empty() == True

def test_queue_len():
    queue = Queue()
    assert len(queue) == 0
    queue.enqueue(1)
    assert len(queue) == 1

def test_queue_contains():
    queue = Queue()
    queue.enqueue(1)
    assert 1 in queue

def test_queue_dequeue_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()

def test_queue_front_empty():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.front()