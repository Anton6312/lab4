from collections import deque
from typing import List, Optional, Set, Dict, Any

class Graph:
    """Класс графа, реализованный через список смежности"""
    
    def __init__(self, directed: bool = False):
        """
        Инициализация графа
        
        """
        self.adjacency_list: Dict[Any, List[Any]] = {}
        self.directed = directed
    
    def add_vertex(self, vertex: Any) -> None:
        """Добавление вершины в граф"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, vertex1: Any, vertex2: Any) -> None:
        """
        Добавление ребра между вершинами
        
        Args:
            vertex1: Первая вершина
            vertex2: Вторая вершина
        """
        # Добавляем вершины, если их еще нет
        self.add_vertex(vertex1)
        self.add_vertex(vertex2)
        
        # Добавляем ребро от vertex1 к vertex2
        if vertex2 not in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].append(vertex2)
        
        # Если граф неориентированный, добавляем обратное ребро
        if not self.directed and vertex1 not in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].append(vertex1)
    
    def remove_edge(self, vertex1: Any, vertex2: Any) -> None:
        """Удаление ребра между вершинами"""
        if vertex1 in self.adjacency_list and vertex2 in self.adjacency_list[vertex1]:
            self.adjacency_list[vertex1].remove(vertex2)
        
        if not self.directed and vertex2 in self.adjacency_list and vertex1 in self.adjacency_list[vertex2]:
            self.adjacency_list[vertex2].remove(vertex1)
    
    def remove_vertex(self, vertex: Any) -> None:
        """Удаление вершины из графа"""
        if vertex in self.adjacency_list:
            # Удаляем все ребра, ведущие к этой вершине
            for v in self.adjacency_list:
                if vertex in self.adjacency_list[v]:
                    self.adjacency_list[v].remove(vertex)
            
            # Удаляем саму вершину
            del self.adjacency_list[vertex]
    
    def get_neighbors(self, vertex: Any) -> List[Any]:
        """Получение списка соседей вершины"""
        return self.adjacency_list.get(vertex, [])
    
    def has_vertex(self, vertex: Any) -> bool:
        """Проверка наличия вершины в графе"""
        return vertex in self.adjacency_list
    
    def has_edge(self, vertex1: Any, vertex2: Any) -> bool:
        """Проверка наличия ребра между вершинами"""
        return (vertex1 in self.adjacency_list and 
                vertex2 in self.adjacency_list[vertex1])
    
    def get_vertices(self) -> List[Any]:
        """Получение списка всех вершин"""
        return list(self.adjacency_list.keys())
    
    def get_edges(self) -> List[tuple]:
        """Получение списка всех ребер"""
        edges = []
        for vertex in self.adjacency_list:
            for neighbor in self.adjacency_list[vertex]:
                # Для неориентированного графа добавляем только одно направление
                if not self.directed:
                    if (neighbor, vertex) not in edges:
                        edges.append((vertex, neighbor))
                else:
                    edges.append((vertex, neighbor))
        return edges
    
    def bfs(self, start_vertex: Any, target: Optional[Any] = None) -> List[Any]:
        """
        Обход графа в ширину
        
        Args:
            start_vertex: Вершина, с которой начинается обход
            target: Целевая вершина для поиска
        
        Returns:
            Список вершин в порядке обхода BFS
        """
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        queue = deque([start_vertex])
        result = []
        
        while queue:
            vertex = queue.popleft()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Если нашли целевую вершину
                if target is not None and vertex == target:
                    return result
                
                # Добавляем всех непосещенных соседей в очередь
                for neighbor in self.adjacency_list[vertex]:
                    if neighbor not in visited:
                        queue.append(neighbor)
        
        return result
    
    def dfs(self, start_vertex: Any, target: Optional[Any] = None) -> List[Any]:
        """
        Обход графа в глубину
        
        Args:
            start_vertex: Вершина, с которой начинается обход
            target: Целевая вершина для поиска
        
        Returns:
            Список вершин в порядке обхода DFS
        """
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        stack = [start_vertex]
        result = []
        
        while stack:
            vertex = stack.pop()
            
            if vertex not in visited:
                visited.add(vertex)
                result.append(vertex)
                
                # Если нашли целевую вершину
                if target is not None and vertex == target:
                    return result
                
                # Добавляем соседей в стек в обратном порядке
                # для соответствия рекурсивному порядку обхода
                for neighbor in reversed(self.adjacency_list[vertex]):
                    if neighbor not in visited:
                        stack.append(neighbor)
        
        return result
    
    def dfs_recursive(self, start_vertex: Any, target: Optional[Any] = None) -> List[Any]:
        """
        Рекурсивный обход графа в глубину
        
        Args:
            start_vertex: Вершина, с которой начинается обход
            target: Целевая вершина для поиска
        
        Returns:
            Список вершин в порядке обхода DFS
        """
        if start_vertex not in self.adjacency_list:
            return []
        
        visited = set()
        result = []
        
        def dfs_helper(vertex: Any) -> bool:
            """Вспомогательная рекурсивная функция для DFS"""
            if vertex in visited:
                return False
            
            visited.add(vertex)
            result.append(vertex)
            
            # Если нашли целевую вершину
            if target is not None and vertex == target:
                return True
            
            # Рекурсивно посещаем всех соседей
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    if dfs_helper(neighbor):
                        return True
            
            return False
        
        dfs_helper(start_vertex)
        return result
    
    def bfs_path(self, start_vertex: Any, target: Any) -> Optional[List[Any]]:
        """
        Поиск кратчайшего пути между вершинами с помощью BFS
        
        Args:
            start_vertex: Начальная вершина
            target: Целевая вершина
        
        Returns:
            Список вершин, образующих путь, или None если путь не найден
        """
        if start_vertex not in self.adjacency_list or target not in self.adjacency_list:
            return None
        
        if start_vertex == target:
            return [start_vertex]
        
        visited = set([start_vertex])
        queue = deque([start_vertex])
        parent = {start_vertex: None}
        
        while queue:
            vertex = queue.popleft()
            
            for neighbor in self.adjacency_list[vertex]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    parent[neighbor] = vertex
                    
                    if neighbor == target:
                        # Восстанавливаем путь
                        path = []
                        current = neighbor
                        while current is not None:
                            path.append(current)
                            current = parent[current]
                        return list(reversed(path))
                    
                    queue.append(neighbor)
        
        return None
    
    def __str__(self) -> str:
        """Строковое представление графа"""
        result = []
        result.append(f"Graph (directed: {self.directed})")
        result.append(f"Vertices: {len(self.adjacency_list)}")
        for vertex in self.adjacency_list:
            neighbors = ', '.join(str(n) for n in self.adjacency_list[vertex])
            result.append(f"  {vertex}: [{neighbors}]")
        return '\n'.join(result)


# Пример использования
if __name__ == "__main__":
    # Создаем неориентированный граф
    graph = Graph(directed=False)
    
    # Добавляем вершины и ребра
    graph.add_edge('A', 'B')
    graph.add_edge('A', 'C')
    graph.add_edge('B', 'D')
    graph.add_edge('B', 'E')
    graph.add_edge('C', 'F')
    graph.add_edge('E', 'F')
    
    print(graph)
    print("\nВершины:", graph.get_vertices())
    print("Рёбра:", graph.get_edges())
    
    # Обход в ширину (BFS)
    print("\nBFS обход, начиная с 'A':", graph.bfs('A'))
    
    # Обход в глубину (DFS)
    print("DFS обход (итеративный), начиная с 'A':", graph.dfs('A'))
    print("DFS обход (рекурсивный), начиная с 'A':", graph.dfs_recursive('A'))
    
    # Поиск пути
    print("\nПоиск пути от 'A' до 'F' (BFS):", graph.bfs_path('A', 'F'))
    
    # Создаем ориентированный граф
    digraph = Graph(directed=True)
    
    digraph.add_edge('A', 'B')
    digraph.add_edge('A', 'C')
    digraph.add_edge('B', 'D')
    digraph.add_edge('C', 'D')
    digraph.add_edge('D', 'E')
    
    print(digraph)
    print("\nBFS обход, начиная с 'A':", digraph.bfs('A'))

    print("DFS обход, начиная с 'A':", digraph.dfs('A'))
