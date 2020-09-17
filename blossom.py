# Based on Blossom V paper
# input: graph as adjacency list
# output: number of edges matched
def max_matches(graph):
    matching = [-1] * len(graph)
    path = [0] * len(graph)
    for i in range(0, len(graph)):
        if (matching[i] == -1):
            v = find_path(graph, matching, path, i)
            while (v != -1):
                pv = path[v]
                ppv = matching[pv]
                matching[v] = pv
                matching[pv] = v
                v = ppv
        
    matched = 0
    for i in range(0, len(graph)):
        if (matching[i] != -1):
            matched += 1
    return matched

def find_path(graph, matching, path, root):
    visited = [False] * len(graph)
    base = list(range(0, len(graph)))
    for i in range(0, len(graph)):
        path[i] = -1

    visited[root] = True
    qh = 0
    qt = 0
    q = [0] * len(graph)
    q[qt] = root
    qt += 1
    while (qh < qt):
        v = q[qh]
        qh += 1
        for to in graph[v]:
            if (base[v] == base[to] or matching[v] == to):
                continue
            if (to == root or matching[to] != -1 and path[matching[to]] != -1):
                curr_base = least_common_ancestor(matching, base, path, v, to)
                blossom = [False] * len(graph)
                mark_path(matching, base, blossom, path, v, curr_base, to)
                mark_path(matching, base, blossom, path, to, curr_base, v)
                for i in range(0, len(graph)):
                    if (blossom[base[i]]):
                        base[i] = curr_base
                        if (not visited[i]):
                            visited[i] = True
                            q[qt] = i
                            qt += 1
            elif (path[to] == -1):
                path[to] = v
                if (matching[to] == -1):
                    return to
                to = matching[to]
                visited[to] = True
                q[qt] = to
                qt += 1
    return -1

def least_common_ancestor(matching, base, path, a, b):
    visited = [False] * len(matching)
    while True:
        a = base[a]
        visited[a] = True
        if (matching[a] == -1):
            break
        a = path[matching[a]]
    while True:
        b = base[b]
        visited[b] = True
        if (matching[b] == -1):
            return b
        b = path[matching[b]]

def mark_path(matching, base, blossom, path, v, b, to):
    while (base[v] != b):
        blossom[base[v]] = blossom[base[matching[v]]] = True
        path[v] = to
        to = matching[v]
        v = path[matching[v]]