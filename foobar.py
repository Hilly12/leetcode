import math
import base64
import itertools

# maximum possible integer product
def maxProduct(xs):
    if (len(xs) == 0):
        return 0
    maxSoFar = xs[0]
    minSoFar = xs[0]
    for i in range(1, len(xs)):
        temp = max(max(maxSoFar * xs[i], maxSoFar), max(minSoFar * xs[i], xs[i]))
        minSoFar = min(min(minSoFar * xs[i], minSoFar), min(maxSoFar * xs[i], xs[i]))
        maxSoFar = temp
    return maxSoFar

# (a, b) -> (a + b, b) | (a, a + b)
# how many steps to (x, y) from (1, 1)
def bombBaby(x, y):
    m = int(x)
    f = int(y)
    count = 0
    while (m > 1 and f > 1):
        mult = 1
        if (m > f):
            mult = m // f
            m -= f * mult
        else:
            mult = f // m
            f -= m * mult
        count += mult

    if (m == 1 and f == 1):
        return str(count)
    elif (m == 1):
        return str(count + f - 1)
    elif (f == 1):
        return str(count + m - 1)
    return "impossible"

# distinct partition problem
def staircase(n):
    table =  [([0] * (n + 1)) for i in range(n + 2)]
    return dp(n, 1, table) - 1
    
def dp(n, k, table):
    if (n == 0):
        return 1
    if (n < k):
        return 0
    if (table[n][k] != 0):
        return table[n][k]
    table[n][k] = dp(n - k, k + 1, table) + dp(n, k + 1, table)
    return table[n][k]

# bfs shortest path, but your allowed to clear 1 tile
def sp(mp):
    queue = [(0, 0, 0, 0)]
    w = len(mp)
    h = len(mp[0])
    visited = [[[False for i in range(2)] for y in range(h)] for x in range(w)]
    
    while (len(queue) > 0):
        x, y, wallReplaced, steps = queue.pop(0)
        if (0 <= x and x < w and 0 <= y and y < h):
            if (x == w - 1 and y == h - 1):
                return steps + 1
            if ((not visited[x][y][wallReplaced]) and (mp[x][y] == 0 or wallReplaced == 0)):
                wallReplaced |= mp[x][y]
                queue.append((x - 1, y, wallReplaced, steps + 1))
                queue.append((x + 1, y, wallReplaced, steps + 1))
                queue.append((x, y - 1, wallReplaced, steps + 1))
                queue.append((x, y + 1, wallReplaced, steps + 1))
                visited[x][y][wallReplaced] = True
    
    return 0

# (1, 4) -> (2, 3) -> (4, 1) -> ...
# lower goes all in, bigger always loses
# finds looping pairs given list and creates maximal matching
# using the blossom algorithm to find out least pairs
# unmatched
def distract(banana_list):
    banana_graph = [[] for i in banana_list]
    for i in range(0, len(banana_list)):
        for j in range(i + 1, len(banana_list)):
            if (loops(banana_list[i], banana_list[j])):
                banana_graph[i].append(j)
                banana_graph[j].append(i)

    return len(banana_list) - max_matches(banana_graph)

def loops(x, y):
    n = (x + y) // gcd(x, y)
    return n & (n - 1) != 0

def gcd(x, y):
    while(y):
        x, y = y, x % y
    return x

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


# times to collect items given a graph
# computes maximum gain in given limit
def run(times, times_limit):
    bunnies = len(times) - 2

    for k in range(0, len(times)):
        for i in range(0, len(times)):
            for j in range(0, len(times)):
                times[i][j] = min(times[i][j], times[i][k] + times[k][j])

    for i in range(0, len(times)):
        if (times[i][i] < 0):
            return list(range(0, bunnies))

    most_rescued = []
    queue = [([i], times[0][i + 1]) for i in range(0, bunnies)]
    while (len(queue) > 0):
        rescued, time = queue.pop(0)
        last_bunny = rescued[-1] + 1
        finish_time = times[last_bunny][-1] + time

        if (finish_time > times_limit):
            continue

        if (finish_time <= times_limit and len(rescued) > len(most_rescued)):
            most_rescued = rescued

        for i in range(0, bunnies):
            if (not i in rescued):
                queue.append((rescued + [i], time + times[last_bunny][i + 1]))

    return sorted(most_rescued)

# computes sum of floor(i * sqrt(2))
def dodge(s):
    return str(sn(int(s)))

# replace int with long in python 2
def sn(n):
    if (n <= 40):
        return sum([int((2 ** 0.5) * i) for i in range(1, n + 1)])
    fr = int('41421356237309504880168872420969807856967187537694807317667973799073247846210703885038753432764157273')
    x = n * fr // (10 ** 101)
    return n * x + ((n - x) * (n + x + 1) // 2) - sn(x)

def decrypt(username, message):
    key = bytes(username, 'utf-8')
    return bytes(a ^ b for a, b in zip(base64.b64decode(message), itertools.cycle(key)))

print(decrypt('aahilamehta', 'GkYbHA8CCBYbU0FbQU8OHgQMEU9YQUYCBwUABAwCHRFGQVtITgkSGQANGQQFRkRJSwQLAwcGFRJG SFNMRgQLCwYEBQgKBQlGQUVPFQIJCA0fCQwICxxTQVtBTxwCDQIGAxEFRk1ITh4ADwcBABJGQVJJ SxIMAw1TTUFGDgYDRk1fSFMWCA9JThE='))