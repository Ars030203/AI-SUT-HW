def custom_dijkstra(graph, start_distances, target, parent_nodes=None, coefficient=1, comparison_target=None):

    distances = start_distances.copy()

    waiting_list = set()
    for i in range(len(start_distances)):
        waiting_list.add((distances[i], i))

    while waiting_list:
        cost, node = min(waiting_list)
        waiting_list.remove((cost, node))

        if node == target:
            break

        for neighbor, weight in graph[node]:
            new_cost = distances[node] + weight * coefficient
            if new_cost < distances[neighbor]:
                waiting_list.remove((distances[neighbor], neighbor))
                distances[neighbor] = new_cost
                if parent_nodes:
                    parent_nodes[neighbor] = node
                waiting_list.add((distances[neighbor], neighbor))
                
                if comparison_target and neighbor == target and distances[neighbor] < comparison_target:
                    return distances, parent_nodes, True

    return distances, parent_nodes, False


def main():
    num_cases = int(input())
    for _ in range(num_cases):
        num_nodes, num_edges = map(int, input().split())

        graph = [[] for _ in range(num_nodes)]
        for _ in range(num_edges):
            u, v, w = map(int, input().split())
            u -= 1
            v -= 1
            graph[u].append((v, w))
            graph[v].append((u, w))

        num_tintin_targets = int(input())
        tintin_targets = [a-1 for a in map(int, input().split())]

        num_criminals = int(input())
        criminal_nodes = [a-1 for a in map(int, input().split())]

        start, goal = map(int, input().split())
        start -= 1
        goal -= 1

        distances_to_goal, parent_nodes, _ = custom_dijkstra(graph,
            start_distances=[0 if i == start else 1e18 for i in range(num_nodes)],
            parent_nodes=[-1 for _ in range(num_nodes)],
            target=goal)

        distances_to_criminals, _, tintin_found = custom_dijkstra(graph,
            start_distances=[0 if i in criminal_nodes else 1e18 for i in range(num_nodes)],
            target=goal,
            comparison_target=distances_to_goal[goal])

        if not tintin_found:
            initial_car_distances = [goal if i in tintin_targets else 1e18 for i, g in enumerate(distances_to_criminals)]
            distances_to_backup, _, tintin_found = custom_dijkstra(graph,
                start_distances=initial_car_distances,
                coefficient=1/2,
                target=goal,
                comparison_target=distances_to_goal[goal])

        if tintin_found or distances_to_goal[goal] > min(distances_to_criminals[goal], distances_to_backup[goal]):
            print("Unlucky Tintin")
        else:
            print(distances_to_goal[goal])
            path = [goal+1]
            while goal != start:
                goal = parent_nodes[goal]
                path.append(goal+1)

            print(len(path))
            print(*path[::-1])


if __name__ == '__main__':
    main()