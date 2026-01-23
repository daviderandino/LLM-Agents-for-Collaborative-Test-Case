import pytest
from data.input_code.d03_stack import *

def test_T1_STACK_PUSH_PEEK():
    stack = Stack()
    stack.push(5)
    assert stack.peek() == 5

def test_T2_STACK_POP_SEQUENCE():
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    assert stack.pop() == 3
    assert stack.size() == 2
    assert stack.pop() == 2
    assert stack.pop() == 1
    assert stack.is_empty() is True

def test_T3_STACK_EMPTY_EXCEPTIONS():
    stack = Stack()
    with pytest.raises(IndexError):
        stack.pop()
    with pytest.raises(IndexError):
        stack.peek()

def test_T4_STACK_CLEAR_CONTAINS():
    stack = Stack()
    stack.push("a")
    stack.push("b")
    stack.clear()
    assert stack.is_empty() is True
    assert ("a" in stack) is False
    assert len(stack) == 0

def test_T5_QUEUE_ENQUEUE_FRONT():
    queue = Queue()
    queue.enqueue("x")
    assert queue.front() == "x"

def test_T6_QUEUE_DEQUEUE_SEQUENCE():
    queue = Queue()
    queue.enqueue("a")
    queue.enqueue("b")
    assert queue.dequeue() == "a"
    assert queue.front() == "b"
    assert queue.dequeue() == "b"
    assert queue.is_empty() is True

def test_T7_QUEUE_EMPTY_EXCEPTIONS():
    queue = Queue()
    with pytest.raises(IndexError):
        queue.dequeue()
    with pytest.raises(IndexError):
        queue.front()

def test_T8_QUEUE_CLEAR_CONTAINS():
    queue = Queue()
    queue.enqueue(1)
    queue.enqueue(2)
    queue.clear()
    assert queue.is_empty() is True
    assert (1 in queue) is False
    assert len(queue) == 0

def test_T9_STACK_SIZE():
    stack = Stack()
    for item in [1, 2, 3]:
        stack.push(item)
    assert stack.size() == 3


def test_T10_STACK_LEN():
    stack = Stack()
    for item in [1, 2]:
        stack.push(item)
    assert len(stack) == 2


def test_T11_STACK_CONTAINS():
    stack = Stack()
    for item in [5]:
        stack.push(item)
    assert (5 in stack) is True


def test_T12_QUEUE_SIZE():
    queue = Queue()
    for item in ["a", "b", "c"]:
        queue.enqueue(item)
    assert queue.size() == 3


def test_T13_QUEUE_LEN():
    queue = Queue()
    for item in [1, 2]:
        queue.enqueue(item)
    assert len(queue) == 2


def test_T14_QUEUE_CONTAINS():
    queue = Queue()
    for item in [10]:
        queue.enqueue(item)
    assert (10 in queue) is True