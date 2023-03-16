import heapq

def djk(adj, init, dest, parents=None, coeff=1, cmp=None):
    dist = init.copy()
    q = [(dist[i], i) for i in range(len(init))]
    while q:
        g, v = heapq.heappop(q)
        if v == dest: break
        if g > dist[v]: continue
        for u, w in adj[v]:
            if dist[v] + w * coeff < dist[u]:
                dist[u] = dist[v] + w * coeff
                if parents: parents[u] = v
                heapq.heappush(q, (dist[u], u))
                if cmp and u == dest and dist[u] < cmp: return dist, parents, True
    return dist, parents, False

def main():
    for _ in range(int(input())):
        n, m = map(int, input().split())
        adj = [[] for _ in range(n)]
        for i in range(m):
            u, v, g = map(int, input().split())
            u -= 1
            v -= 1
            adj[u].append((v, g))
            adj[v].append((u, g))
        t = int(input())
        criminals = [a-1 for a in map(int, input().split())]
        c = int(input())
        cars = [a-1 for a in map(int, input().split())]
        s, g = map(int, input().split())
        s -= 1
        g -= 1
        dist_t, parents, _ = djk(adj, [0 if i == s else 1e18 for i in range(n)], g, [-1 for _ in range(n)])
        dist_c, _, f_t = djk(adj, [0 if i in criminals else 1e18 for i in range(n)], g, cmp=dist_t[g])
        if not f_t:
            dist_bs, _, f_t = djk(adj, [g if i in cars else 1e18 for i in range(n)], g, 1/2, cmp=dist_t[g])
        if f_t or dist_t[g] > min(dist_c[g], dist_bs[g]):
            print("Poor Tintin")
        else:
            print(dist_t[g])
            path = [g+1]
            while g != s:
                g = parents[g]
                path.append(g+1)
            print(len(path))
            print(*path[::-1])

if __name__ == '__main__':
    main()