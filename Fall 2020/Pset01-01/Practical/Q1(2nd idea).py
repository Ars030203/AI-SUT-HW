from collections import deque
from heapq import heappop, heappush


def find_shortest_path(graph, start, end):
    distances = {vertex: float('inf') for vertex in graph}
    previous_vertices = {vertex: None for vertex in graph}
    distances[start] = 0

    
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_vertex = heappop(priority_queue)

        if current_distance > distances[current_vertex]:
            continue

        for neighbor, weight in graph[current_vertex].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_vertices[neighbor] = current_vertex
                heappush(priority_queue, (distance, neighbor))

    shortest_path = []
    current_vertex = end
    while current_vertex is not None:
        shortest_path.append(current_vertex)
        current_vertex = previous_vertices[current_vertex]

    shortest_path.reverse()
    return shortest_path


def reduce_path_weights(graph, path):
    for i in range(len(path) - 1):
        u, v = path[i], path[i + 1]
        graph[u][v] = 0


def find_paths_with_commonality(graph, a, b, c, d):
    paths_ab = []
    paths_cd = []

 
    paths_ab.append(find_shortest_path(graph, a, b))


    paths_cd.append(find_shortest_path(graph, c, d))

    max_commonality = 0
    selected_ab = None
    selected_cd = None


    for path_ab in paths_ab:
        for path_cd in paths_cd:
            common_vertices = set(path_ab) & set(path_cd)
            commonality = len(common_vertices)
            if commonality > max_commonality:
                max_commonality = commonality
                selected_ab = path_ab
                selected_cd = path_cd

    return selected_ab, selected_cd


graph = {
    'a': {'b': 3, 'c': 2},
    'b': {'d': 4},
    'c': {'d': 1},
    'd': {}
}
a = 'a'
b = 'd'
c = 'a'
d = 'b'


path_ab, path_cd = find_paths_with_commonality(graph, a, b, c, d)

reduce_path_weights(graph, path_ab)


print("Modified Graph:")
print(graph)

print("Path from 'a' to 'b':", path_ab)
print("Path from 'c' to 'd':", path_cd)