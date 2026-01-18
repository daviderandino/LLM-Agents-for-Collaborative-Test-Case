import pytest
from data.input_code.d03_stack import *

# ---------- Stack Tests ----------

def test_stack_initialization():
    s = Stack()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

def test_stack_push_and_state():
    s = Stack()
    s.push(5)
    assert not s.is_empty()
    assert s.size() == 1
    assert len(s) == 1
    assert 5 in s
    assert s.peek() == 5

def test_stack_pop():
    s = Stack()
    s.push(5)
    popped = s.pop()
    assert popped == 5
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_clear():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

# ---------- Queue Tests ----------

def test_queue_initialization():
    q = Queue()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

def test_queue_enqueue_and_state():
    q = Queue()
    q.enqueue(5)
    assert not q.is_empty()
    assert q.size() == 1
    assert len(q) == 1
    assert 5 in q
    assert q.front() == 5

def test_queue_dequeue():
    q = Queue()
    q.enqueue(5)
    dequeued = q.dequeue()
    assert dequeued == 5
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_clear():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0