import pytest
from data.input_code.d03_stack import Stack, Queue


class TestStack:
    def test_push_pop_peek_and_size(self):
        s = Stack()
        # push multiple items
        s.push(1)
        s.push(2)
        s.push(3)
        assert s.size() == 3
        assert s.is_empty() is False
        # peek returns last without removal
        assert s.peek() == 3
        assert s.size() == 3
        # pop returns last and reduces size
        assert s.pop() == 3
        assert s.size() == 2
        # peek again
        assert s.peek() == 2
        # pop remaining items
        assert s.pop() == 2
        assert s.pop() == 1
        assert s.is_empty() is True
        assert s.size() == 0

    def test_pop_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError, match="Pop from empty stack"):
            s.pop()

    def test_peek_empty_raises(self):
        s = Stack()
        with pytest.raises(IndexError, match="Peek from empty stack"):
            s.peek()

    def test_is_empty_size_clear_and_len(self):
        s = Stack()
        assert s.is_empty() is True
        assert s.size() == 0
        assert len(s) == 0
        s.push("a")
        assert s.is_empty() is False
        assert s.size() == 1
        assert len(s) == 1
        s.clear()
        assert s.is_empty() is True
        assert s.size() == 0
        assert len(s) == 0



class TestQueue:
    def test_enqueue_dequeue_front_and_size(self):
        q = Queue()
        q.enqueue("x")
        q.enqueue("y")
        q.enqueue("z")
        assert q.size() == 3
        assert q.is_empty() is False
        # front returns first without removal
        assert q.front() == "x"
        assert q.size() == 3
        # dequeue returns first and reduces size
        assert q.dequeue() == "x"
        assert q.size() == 2
        # front again
        assert q.front() == "y"
        # dequeue remaining items
        assert q.dequeue() == "y"
        assert q.dequeue() == "z"
        assert q.is_empty() is True
        assert q.size() == 0

    def test_dequeue_empty_raises(self):
        q = Queue()
        with pytest.raises(IndexError, match="Dequeue from empty queue"):
            q.dequeue()

    def test_front_empty_raises(self):
        q = Queue()
        with pytest.raises(IndexError, match="Front from empty queue"):
            q.front()

    def test_is_empty_size_clear_and_len(self):
        q = Queue()
        assert q.is_empty() is True
        assert q.size() == 0
        assert len(q) == 0
        q.enqueue(1)
        assert q.is_empty() is False
        assert q.size() == 1
        assert len(q) == 1
        q.clear()
        assert q.is_empty() is True
        assert q.size() == 0
        assert len(q) == 0

