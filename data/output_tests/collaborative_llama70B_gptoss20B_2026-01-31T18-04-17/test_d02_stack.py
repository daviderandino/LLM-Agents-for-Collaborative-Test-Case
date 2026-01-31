import pytest
from data.input_code.d02_stack import *

# -------------------- Stack Tests --------------------

def test_stack_init():
    s = Stack()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0

def test_stack_push_and_size():
    s = Stack()
    s.push(5)
    assert s.size() == 1
    assert len(s) == 1
    assert s.is_empty() is False

def test_stack_pop():
    s = Stack()
    s.push(5)
    assert s.pop() == 5
    assert s.is_empty() is True
    assert s.size() == 0

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek():
    s = Stack()
    s.push(5)
    assert s.peek() == 5
    assert s.size() == 1  # peek should not remove

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty():
    s = Stack()
    assert s.is_empty() is True
    s.push(1)
    assert s.is_empty() is False

def test_stack_len():
    s = Stack()
    assert len(s) == 0
    s.push(1)
    assert len(s) == 1

def test_stack_contains():
    s = Stack()
    s.push(5)
    assert 5 in s
    assert 3 not in s

def test_stack_clear():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.is_empty() is True
    assert s.size() == 0
    assert len(s) == 0
    assert 5 not in s

# -------------------- Queue Tests --------------------

def test_queue_init():
    q = Queue()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0

def test_queue_enqueue_and_size():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1
    assert len(q) == 1
    assert q.is_empty() is False

def test_queue_dequeue():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5
    assert q.is_empty() is True
    assert q.size() == 0

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5
    assert q.size() == 1  # front should not remove

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty():
    q = Queue()
    assert q.is_empty() is True
    q.enqueue(1)
    assert q.is_empty() is False

def test_queue_len():
    q = Queue()
    assert len(q) == 0
    q.enqueue(1)
    assert len(q) == 1

def test_queue_contains():
    q = Queue()
    q.enqueue(5)
    assert 5 in q
    assert 3 not in q

def test_queue_clear():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q.is_empty() is True
    assert q.size() == 0
    assert len(q) == 0
    assert 5 not in q