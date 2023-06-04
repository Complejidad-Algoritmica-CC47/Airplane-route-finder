import networkx as nx

def bfs(graph, start_node, end_node):
    print("Iniciando BFS...")

    visited = set()
    queue = []

    visited.add(start_node)
    queue.append([start_node])

    while queue:
        path = queue.pop(0)
        node = path[-1]

        if node == end_node:
            return path  # Retorna el camino si se encuentra el nodo final

        neighbors = graph.neighbors(node)  # Obtiene los vecinos del nodo actual

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)

    return None  # Retorna None si no se encuentra un camino

