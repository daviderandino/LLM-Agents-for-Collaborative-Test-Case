import pytest
from data.input_code.d02_stack import Stack, Queue


# --------------------- Stack Tests --------------------- #

def test_stack_push_and_pop_order_and_size():
    s = Stack()
    # Initially empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

    # Push elements
    s.push(1)
    s.push(2)
    s.push(3)
    assert not s.is_empty()
    assert s.size() == 3
    assert len(s) == 3

    # Pop elements in LIFO order
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    # After popping all, stack should be empty
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0

def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()

def test_stack_peek_and_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()
    s.push('a')
    assert s.peek() == 'a'
    # Peek should not remove the item
    assert s.size() == 1
    assert s.pop() == 'a'

def test_stack_contains_and_clear_and_len():
    s = Stack()
    s.push('x')
    s.push('y')
    s.push('z')
    assert 'x' in s
    assert 'y' in s
    assert 'z' in s
    assert 'a' not in s
    assert '' not in s
    assert None not in s

    # Clear the stack
    s.clear()
    assert s.is_empty()
    assert s.size() == 0
    assert len(s) == 0
    assert 'x' not in s
    assert 'y' not in s

def test_stack_push_none_and_empty_string():
    s = Stack()
    s.push(None)
    s.push('')
    assert s.size() == 2
    assert s.peek() == ''
    assert s.pop() == ''
    assert s.pop() == None
    assert s.is_empty()

def test_stack_pop_and_peek_after_clear():
    s = Stack()
    s.push(10)
    s.clear()
    with pytest.raises(IndexError, match="Pop from empty stack"):
        s.pop()
    with pytest.raises(IndexError, match="Peek from empty stack"):
        s.peek()


# --------------------- Queue Tests --------------------- #

def test_queue_enqueue_and_dequeue_order_and_size():
    q = Queue()
    # Initially empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

    # Enqueue elements
    q.enqueue('a')
    q.enqueue('b')
    q.enqueue('c')
    assert not q.is_empty()
    assert q.size() == 3
    assert len(q) == 3

    # Dequeue elements in FIFO order
    assert q.dequeue() == 'a'
    assert q.dequeue() == 'b'
    assert q.dequeue() == 'c'
    # After dequeuing all, queue should be empty
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0

def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()

def test_queue_front_and_front_empty_raises():
    q = Queue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()
    q.enqueue(42)
    assert q.front() == 42
    # Front should not remove the item
    assert q.size() == 1
    assert q.dequeue() == 42

def test_queue_contains_and_clear_and_len():
    q = Queue()
    q.enqueue('foo')
    q.enqueue('bar')
    q.enqueue('baz')
    assert 'foo' in q
    assert 'bar' in q
    assert 'baz' in q
    assert 'qux' not in q
    assert '' not in q
    assert None not in q

    # Clear the queue
    q.clear()
    assert q.is_empty()
    assert q.size() == 0
    assert len(q) == 0
    assert 'foo' not in q
    assert 'bar' not in q

def test_queue_enqueue_none_and_empty_string():
    q = Queue()
    q.enqueue(None)
    q.enqueue('')
    assert q.size() == 2
    assert q.front() == None
    assert q.dequeue() == None
    assert q.dequeue() == ''
    assert q.is_empty()

def test_queue_dequeue_and_front_after_clear():
    q = Queue()
    q.enqueue('x')
    q.clear()
    with pytest.raises(IndexError, match="Dequeue from empty queue"):
        q.dequeue()
    with pytest.raises(IndexError, match="Front from empty queue"):
        q.front()