import pytest
from data.input_code.d02_stack import Stack, Queue

@pytest.mark.parametrize('target, input, expected', [
    ('Stack.__init__', {}, None),
    ('Stack.push', {'item': 1}, None),
    ('Stack.pop', {'item': 1}, 1),
    ('Stack.peek', {'item': 1}, 1),
    ('Stack.is_empty', {}, True),
    ('Stack.size', {}, 0),
    ('Stack.clear', {}, None),
    ('Stack.__len__', {}, 0),
    ('Stack.__contains__', {'item': 1}, True),
    ('Queue.__init__', {}, None),
    ('Queue.enqueue', {'item': 1}, None),
    ('Queue.dequeue', {'item': 1}, 1),
    ('Queue.front', {'item': 1}, 1),
    ('Queue.is_empty', {}, True),
    ('Queue.size', {}, 0),
    ('Queue.clear', {}, None),
    ('Queue.__len__', {}, 0),
    ('Queue.__contains__', {'item': 1}, True),
])
def test_stack_queue(target, input, expected):
    if target == 'Stack.__init__':
        stack = Stack()
        assert stack._items == []
    elif target == 'Stack.push':
        stack = Stack()
        stack.push(input['item'])
        assert stack._items == [input['item']]
    elif target == 'Stack.pop':
        stack = Stack()
        stack.push(input['item'])
        assert stack.pop() == input['item']
    elif target == 'Stack.peek':
        stack = Stack()
        stack.push(input['item'])
        assert stack.peek() == input['item']
    elif target == 'Stack.is_empty':
        stack = Stack()
        assert stack.is_empty() == expected
    elif target == 'Stack.size':
        stack = Stack()
        assert stack.size() == expected
    elif target == 'Stack.clear':
        stack = Stack()
        stack.clear()
        assert stack._items == []
    elif target == 'Stack.__len__':
        stack = Stack()
        assert len(stack) == expected
    elif target == 'Stack.__contains__':
        stack = Stack()
        stack.push(input['item'])
        assert (input['item'] in stack) == expected
    elif target == 'Queue.__init__':
        queue = Queue()
        assert queue._items == []
    elif target == 'Queue.enqueue':
        queue = Queue()
        queue.enqueue(input['item'])
        assert queue._items == [input['item']]
    elif target == 'Queue.dequeue':
        queue = Queue()
        queue.enqueue(input['item'])
        assert queue.dequeue() == input['item']
    elif target == 'Queue.front':
        queue = Queue()
        queue.enqueue(input['item'])
        assert queue.front() == input['item']
    elif target == 'Queue.is_empty':
        queue = Queue()
        assert queue.is_empty() == expected
    elif target == 'Queue.size':
        queue = Queue()
        assert queue.size() == expected
    elif target == 'Queue.clear':
        queue = Queue()
        queue.clear()
        assert queue._items == []
    elif target == 'Queue.__len__':
        queue = Queue()
        assert len(queue) == expected
    elif target == 'Queue.__contains__':
        queue = Queue()
        queue.enqueue(input['item'])
        assert (input['item'] in queue) == expected

def test_stack_pop_error():
    with pytest.raises(IndexError):
        stack = Stack()
        stack.pop()

def test_stack_peek_error():
    with pytest.raises(IndexError):
        stack = Stack()
        stack.peek()

def test_queue_dequeue_error():
    with pytest.raises(IndexError):
        queue = Queue()
        queue.dequeue()

def test_queue_front_error():
    with pytest.raises(IndexError):
        queue = Queue()
        queue.front()