class Stack:
    def __init__(self):
        self._items = []
    
    def push(self, item):
        self._items.append(item)
    
    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()
    
    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self._items[-1]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def clear(self):
        self._items = []
    
    def __len__(self):
        return len(self._items)
    
    def __contains__(self, item):
        return item in self._items


class Queue:
    def __init__(self):
        self._items = []
    
    def enqueue(self, item):
        self._items.append(item)
    
    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.pop(0)
    
    def front(self):
        if self.is_empty():
            raise IndexError("Front from empty queue")
        return self._items[0]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def clear(self):
        self._items = []
    
    def __len__(self):
        return len(self._items)
    
    def __contains__(self, item):
        return item in self._items
