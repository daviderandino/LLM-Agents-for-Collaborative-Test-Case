import pytest
from data.input_code.02_stack import *

# Stack tests
def test_stack_init():
    stack = Stack()
    assert stack.is_empty() == True

def test_stack_push_and_pop():
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

@pytest.mark.parametrize("item", [5])
def test_stack_contains(item):
    stack = Stack()
    stack.push(item)
    assert item in stack

@pytest.mark.parametrize("item", [10])
def test_stack_not_contains(item):
    stack = Stack()
    stack.push(5)
    assert item not in stack

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

def test_stack_is_empty():
    stack = Stack()
    assert stack.is_empty() == True

def test_stack_is_not_empty():
    stack = Stack()
    stack.push(5)
    assert stack.is_empty() == False

# Queue tests
def test_queue_init():
    queue = Queue()
    assert queue.is_empty() == True

def test_queue_enqueue_and_dequeue():
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

@pytest.mark.parametrize("item", [5])
def test_queue_contains(item):
    queue = Queue()
    queue.enqueue(item)
    assert item in queue

@pytest.mark.parametrize("item", [10])
def test_queue_not_contains(item):
    queue = Queue()
    queue.enqueue(5)
    assert item not in queue

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

def test_queue_is_empty():
    queue = Queue()
    assert queue.is_empty() == True

def test_queue_is_not_empty():
    queue = Queue()
    queue.enqueue(5)
    assert queue.is_empty() == False