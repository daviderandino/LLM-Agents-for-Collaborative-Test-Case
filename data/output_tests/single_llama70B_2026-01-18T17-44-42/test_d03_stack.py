import pytest
from data.input_code.d03_stack import Stack, Queue

class TestStack:
    def test_init(self):
        stack = Stack()
        assert stack._items == []

    def test_push(self):
        stack = Stack()
        stack.push(1)
        assert stack._items == [1]

    def test_pop(self):
        stack = Stack()
        stack.push(1)
        assert stack.pop() == 1
        assert stack._items == []

    def test_pop_empty(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.pop()

    def test_peek(self):
        stack = Stack()
        stack.push(1)
        assert stack.peek() == 1
        assert stack._items == [1]

    def test_peek_empty(self):
        stack = Stack()
        with pytest.raises(IndexError):
            stack.peek()

    def test_is_empty(self):
        stack = Stack()
        assert stack.is_empty() == True
        stack.push(1)
        assert stack.is_empty() == False

    def test_size(self):
        stack = Stack()
        assert stack.size() == 0
        stack.push(1)
        assert stack.size() == 1

    def test_clear(self):
        stack = Stack()
        stack.push(1)
        stack.clear()
        assert stack._items == []

    def test_len(self):
        stack = Stack()
        assert len(stack) == 0
        stack.push(1)
        assert len(stack) == 1

    def test_contains(self):
        stack = Stack()
        stack.push(1)
        assert 1 in stack
        assert 2 not in stack

class TestQueue:
    def test_init(self):
        queue = Queue()
        assert queue._items == []

    def test_enqueue(self):
        queue = Queue()
        queue.enqueue(1)
        assert queue._items == [1]

    def test_dequeue(self):
        queue = Queue()
        queue.enqueue(1)
        assert queue.dequeue() == 1
        assert queue._items == []

    def test_dequeue_empty(self):
        queue = Queue()
        with pytest.raises(IndexError):
            queue.dequeue()

    def test_front(self):
        queue = Queue()
        queue.enqueue(1)
        assert queue.front() == 1
        assert queue._items == [1]

    def test_front_empty(self):
        queue = Queue()
        with pytest.raises(IndexError):
            queue.front()

    def test_is_empty(self):
        queue = Queue()
        assert queue.is_empty() == True
        queue.enqueue(1)
        assert queue.is_empty() == False

    def test_size(self):
        queue = Queue()
        assert queue.size() == 0
        queue.enqueue(1)
        assert queue.size() == 1

    def test_clear(self):
        queue = Queue()
        queue.enqueue(1)
        queue.clear()
        assert queue._items == []

    def test_len(self):
        queue = Queue()
        assert len(queue) == 0
        queue.enqueue(1)
        assert len(queue) == 1

    def test_contains(self):
        queue = Queue()
        queue.enqueue(1)
        assert 1 in queue
        assert 2 not in queue