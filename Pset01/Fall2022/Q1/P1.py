import heapq

N = 0
M = 0

neighbors = [[] for _ in range(20)]

dist = [[0] * 20 for _ in range(20)]

class State:
    def __init__(self, positions):
        self.positions = positions
        self.update_hole()
        self.estimate = 0
        self.passed = 0
        self.get_estimate()

    def is_final(self):
        return all(idx == pos for idx, pos in enumerate(self.positions))

    def __lt__(self, other):
        return -(self.passed + self.estimate) < -(other.passed + other.estimate)

    def hash(self):
        seed = len(self.positions)
        for x in self.positions:
            x = ((x >> 16) ^ x) * 0x45d9f3b * 0x45d9f3b
            x = ((x >> 16) ^ x) * 0x45d9f3b
            x = (x >> 16) ^ x
            seed ^= x + 0x9e3779b9 + (seed << 6) + (seed >> 2)
        return seed

    def distance(self):
        return self.passed

    def get_neighbors(self):
        result = []
        for neighbor in neighbors[self.hole_pos]:
            clone = State(self.positions[:])
            clone.positions[self.hole_pos], clone.positions[neighbor] = clone.positions[neighbor], clone.positions[self.hole_pos]
            clone.update_hole()
            clone.passed += 1
            clone.estimate = 0
            clone.get_estimate()
            result.append(clone)
        return result

    def get_estimate(self):
        if self.estimate == 0:
            for i in range(N):
                if i != self.hole_pos:
                    self.estimate += dist[i][self.positions[i]]
        return self.estimate

    def get_string(self):
        result = f"{self.passed}:{self.passed + self.estimate}\t"
        result += '\t'.join(map(str, self.positions))
        return result

    def update_hole(self):
        self.hole_pos = self.positions.index(0)

def fill_dist():
    for i in range(N):
        for j in range(N):
            if j in neighbors[i]:
                dist[i][j] = 1
            else:
                dist[i][j] = 0 if i == j else float('inf')

    for k in range(N):
        for i in range(N):
            for j in range(N):
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

def solve_astar(initial):
    queue = []
    heapq.heappush(queue, initial)
    weight = {}

    cnt = 0

    while queue:
        cnt += 1
        if cnt > 1e6:
            return -1

        current = heapq.heappop(queue)

        if current.is_final():
            return current.distance()

        for state in current.get_neighbors():
            if state.hash() not in weight or state.distance() < weight[state.hash()]:
                heapq.heappush(queue, state)
                weight[state.hash()] = state.distance()

    return -1

if __name__ == "__main__":
    N, M = map(int, input().split())
    for _ in range(M):
        u, v = map(int, input().split())
        neighbors[u].append(v)
        neighbors[v].append(u)

    positions = [int(input()) for _ in range(N)]

    fill_dist()
    initial = State(positions)
    print(solve_astar(initial))