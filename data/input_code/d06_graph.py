from collections import deque

class Graph:
    def __init__(self, directed=False):
        self.adj = {}
        self.directed = directed
    
    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []
    
    def add_edge(self, v1, v2):
        self.add_vertex(v1)
        self.add_vertex(v2)
        self.adj[v1].append(v2)
        if not self.directed:
            self.adj[v2].append(v1)
    
    def remove_edge(self, v1, v2):
        if v1 in self.adj:
            self.adj[v1] = [v for v in self.adj[v1] if v != v2]
        if not self.directed and v2 in self.adj:
            self.adj[v2] = [v for v in self.adj[v2] if v != v1]
    
    def get_neighbors(self, v):
        return self.adj.get(v, [])
    
    def bfs(self, start):
        if start not in self.adj:
            return []
        visited = set()
        result = []
        queue = deque([start])
        visited.add(start)
        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            for neighbor in self.adj[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)
        return result
    
    def dfs(self, start):
        if start not in self.adj:
            return []
        visited = set()
        result = []
        self._dfs_recursive(start, visited, result)
        return result
    
    def _dfs_recursive(self, v, visited, result):
        visited.add(v)
        result.append(v)
        for neighbor in self.adj[v]:
            if neighbor not in visited:
                self._dfs_recursive(neighbor, visited, result)
    
    def has_path(self, start, end):
        if start not in self.adj or end not in self.adj:
            return False
        visited = set()
        queue = deque([start])
        while queue:
            v = queue.popleft()
            if v == end:
                return True
            visited.add(v)
            for neighbor in self.adj[v]:
                if neighbor not in visited:
                    queue.append(neighbor)
        return False
    
    def vertices(self):
        return list(self.adj.keys())
