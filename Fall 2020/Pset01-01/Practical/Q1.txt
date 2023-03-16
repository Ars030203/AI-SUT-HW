import heapq

inf = 10**18

class Edge:
    def __init__(self, to, cost):
        self.to = to
        self.cost = cost

N = 100000
G = [[] for _ in range(N)]

def input_graph():
    global N, G, S, T, U, V
    N, M = map(int, input().split())
    S, T = map(int, input().split())
    U, V = map(int, input().split())
    S, T, U, V = S-1, T-1, U-1, V-1
    for i in range(M):
        a, b, c = map(int, input().split())
        a, b = a-1, b-1
        G[a].append(Edge(b, c))
        G[b].append(Edge(a, c))

def dijkstra(s, res):
    que = [(0, s)]
    heapq.heapify(que)
    for i in range(N):
        res[i] = inf
    res[s] = 0
    while que:
        c, v = heapq.heappop(que)
        if res[v] < c:
            continue
        for e in G[v]:
            u, nc = e.to, c + e.cost
            if res[u] <= nc:
                continue
            res[u] = nc
            heapq.heappush(que, (nc, u))

def get(v, id, dist):
    res = 0
    if id & 1:
        res += dist[0][v]
    if id & 2:
        res += dist[1][v]
    return res

def solve():
    dist = [[0] * N for _ in range(2)]
    dist2 = [0] * N
    ps = [(0, i) for i in range(N)]
    dp = [[inf] * 4 for _ in range(N)]

    dijkstra(U, dist[0])
    dijkstra(V, dist[1])
    dijkstra(S, dist2)
    ps.sort()

    dp[S][0] = 0
    dp[S][1] = dist[0][S]
    dp[S][2] = dist[1][S]
    dp[S][3] = dist[0][S] + dist[1][S]

    for p in ps:
        v = p[1]
        for e in G[v]:
            u = e.to
            if dist2[v] != dist2[u] + e.cost:
                continue
            for k in range(4):
                for l in range(4):
                    dp[v][k|l] = min(dp[v][k|l], dp[u][k] + get(v, l, dist))

    ans = dp[T][3]
    ans = min(ans, dist[0][V])
    return ans

input_graph()
ans = solve()
print(ans)