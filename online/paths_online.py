from collections import defaultdict
from itertools import combinations
import time
try:
    from Graph import Graph, compute_mst_and_cost
    from FibHeapPrims import prims_mst
except ImportError:
    from .Graph import Graph, compute_mst_and_cost
    from .FibHeapPrims import prims_mst
import math


def FindMin(s, t, max_d, d, p, v):
    answer = math.inf
    if d[s] != d[t]:
        s, t, answer, max_d, d, p, v = Align(s, t, answer, max_d, d, p, v)
    if s == t:
        return answer
    s, t, answer, max_d, d, p, v = Up(s, t, answer, max_d, d, p, v)
    return min([answer, v[s][0], v[t][0]])


def Align(s, t, answer, max_d, d, p, v):
    if d[s] > d[t]:
        s, t = t, s
    for i in range(int(math.log2(max_d)), -1, -1):
        if d[s] <= d[p[t][i]]:
            answer = min(answer, v[t][i])
            t = p[t][0]
    return s, t, answer, max_d, d, p, v


def Up(s, t, answer, max_d, d, p, v):
    for i in range(int(math.log2(max_d)), -1, -1):
        if p[s][i] != p[t][i]:
            answer = min([answer, v[s][i], v[t][i]])
            s = p[s][i]
            t = p[t][i]
    return s, t, answer, max_d, d, p, v


def paths_online(num_nodes, adj_list, pairs):
    time1 = time.time()
    an = {}
    g = Graph(nfverts=num_nodes, graph=adj_list, representation="lists")
    time3 = time.time()
    g = compute_mst_and_cost(prims_mst(g), g)[0]
    time4 = time.time()
    d = [-1] * num_nodes
    d[int(num_nodes/2)] = 0
    queue = [int(num_nodes/2)]
    max_d = 0
    while queue:
        v = queue.pop(0)
        for w in g.graph[v].keys():
            if d[w] == -1:
                queue.append(w)
                d[w] = d[v] + 1
                if d[w] > max_d:
                    max_d = d[w]

    visited = [-1] * num_nodes
    p = [[int(num_nodes/2)] * (int(math.log2(max_d))+1) for _ in range(num_nodes)]
    v = [[math.inf] * (int(math.log2(max_d))+1) for _ in range(num_nodes)]
    visited[int(num_nodes/2)] = 0
    queue = [int(num_nodes/2)]
    while queue:
        ve = queue.pop(0)
        for w in g.graph[ve].keys():
            if visited[w] == -1:
                p[w][0] = ve
                v[w][0] = g.graph[w][ve]
                for i in range(1, int(math.log2(max_d))+1):
                    pp = p[w][i-1]
                    p[w][i] = p[pp][i-1]
                    v[w][i] = min(v[w][i-1], v[pp][i-1])
                    visited[w] = 0
                    queue.append(w)

    for i in range(len(pairs)):
        an[i] = FindMin(pairs[i][0], pairs[i][1], max_d, d, p, v)
    time2 = time.time()
    return an, time2-time1, time4-time3

if __name__ == "__main__":
    gr = []
    num_nodes = 5
    pairs = list(combinations([i for i in range(num_nodes)], 2))

    with open("graph.txt") as file:
        for line in file:
            gr.append([int(i) for i in line.split()])


    adj_list = defaultdict(dict)
    for i in range(len(gr)):
        adj_list[gr[i][0]][gr[i][1]] = gr[i][2]
        adj_list[gr[i][1]][gr[i][0]] = gr[i][2]

    an, t = paths_online(num_nodes=num_nodes, adj_list=adj_list, pairs=pairs)

    for key in an.keys():
        print(pairs[key], an[key])

