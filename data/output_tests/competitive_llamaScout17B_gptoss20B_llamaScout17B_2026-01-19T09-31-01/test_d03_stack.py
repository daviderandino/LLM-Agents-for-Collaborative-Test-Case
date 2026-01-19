import pytest
from data.input_code.d03_stack import *

def test_stack_init():
    s = Stack()
    assert isinstance(s, Stack)

def test_stack_push():
    s = Stack()
    s.push(5)

def test_stack_pop():
    s = Stack()
    s.push(5)
    assert s.pop() == 5

def test_stack_pop_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()

def test_stack_peek():
    s = Stack()
    s.push(5)
    assert s.peek() == 5

def test_stack_peek_empty():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()

def test_stack_is_empty_true():
    s = Stack()
    assert s.is_empty() is True

def test_stack_is_empty_false():
    s = Stack()
    s.push(5)
    assert s.is_empty() is False

def test_stack_size():
    s = Stack()
    s.push(5)
    assert s.size() == 1

def test_stack_clear():
    s = Stack()
    s.push(5)
    s.clear()
    assert s.size() == 0

def test_stack_len():
    s = Stack()
    assert len(s) == 0

def test_stack_contains_true():
    s = Stack()
    s.push(5)
    assert 5 in s

def test_stack_contains_false():
    s = Stack()
    assert 10 not in s

def test_queue_init():
    q = Queue()
    assert isinstance(q, Queue)

def test_queue_enqueue():
    q = Queue()
    q.enqueue(5)

def test_queue_dequeue():
    q = Queue()
    q.enqueue(5)
    assert q.dequeue() == 5

def test_queue_dequeue_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()

def test_queue_front():
    q = Queue()
    q.enqueue(5)
    assert q.front() == 5

def test_queue_front_empty():
    q = Queue()
    with pytest.raises(IndexError):
        q.front()

def test_queue_is_empty_true():
    q = Queue()
    assert q.is_empty() is True

def test_queue_is_empty_false():
    q = Queue()
    q.enqueue(5)
    assert q.is_empty() is False

def test_queue_size():
    q = Queue()
    q.enqueue(5)
    assert q.size() == 1

def test_queue_clear():
    q = Queue()
    q.enqueue(5)
    q.clear()
    assert q.size() == 0

def test_queue_len():
    q = Queue()
    assert len(q) == 0

def test_queue_contains_true():
    q = Queue()
    q.enqueue(5)
    assert 5 in q

def test_queue_contains_false():
    q = Queue()
    assert 10 not in q