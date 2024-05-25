from itertools import combinations
import time
try:
    from dsf import DisjointSetForest
except ImportError:
    from .dsf import DisjointSetForest


def paths_offline(num_nodes, graph, pairs):
    time1 = time.time()
    ind = {i: set() for i in range(num_nodes)}
    answer = {}
    dsf = DisjointSetForest([i for i in range(num_nodes)])
    for i in range(len(pairs)):
        answer[i] = -1000
        ind[pairs[i][0]] = ind.get(pairs[i][0], set()) | {i}
        ind[pairs[i][1]] = ind.get(pairs[i][1], set()) | {i}

    e = sorted(graph, reverse=True, key=lambda x: x[2])
    for edge in e:
        x = dsf.find_set(edge[0])
        y = dsf.find_set(edge[1])
        if x != y:
            x, y = dsf.union(x, y)
            for z in ind[x].intersection(ind[y]):
                answer[z] = edge[2]
            ind[x] = ind[x].symmetric_difference(ind[y])
            ind[y] = set()
    time2 = time.time()
    return answer, time2-time1


if __name__ == "__main__":
    graph = []
    num_nodes = 5
    pairs = list(combinations([i for i in range(num_nodes)], 2))

    with open("graph.txt") as file:
        for line in file:
            graph.append([int(i) for i in line.split()])

    answer, t = paths_offline(num_nodes=num_nodes, graph=graph, pairs=pairs)

    for key in answer.keys():
        print(pairs[key], answer[key])