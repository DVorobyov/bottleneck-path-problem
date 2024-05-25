from itertools import combinations
from collections import defaultdict
import networkx as nx
from offline.paths_offline import paths_offline
from online.paths_online import paths_online
from camerini.camerini import compute_bsgt

ts1 = []
ts2 = []
t2msts = []
ts3 = []
for i in range(10, 1010, 10):
    print(i)
    num_nodes = i
    pairs = list(combinations([i for i in range(num_nodes)], 2))
    pairs = pairs[:10]

    gr = []
    with open(f"./graphs/graph_{i}.dot", "r") as file:
        for line in file:
            gr.append([int(i) for i in line.split()])

    nx_graph = nx.MultiGraph()
    adj_list = defaultdict(dict)
    for i in range(len(gr)):
        adj_list[gr[i][0]][gr[i][1]] = gr[i][2]
        adj_list[gr[i][1]][gr[i][0]] = gr[i][2]
        nx_graph.add_edge(gr[i][0], gr[i][1], capacity=gr[i][2], key=i)

    an1, t1 = paths_offline(num_nodes=num_nodes, graph=gr, pairs=pairs)
    print("offline DONE")
    an2, t2, t2mst = paths_online(num_nodes=num_nodes, adj_list=adj_list, pairs=pairs)
    print("online DONE")
    ts1.append(t1)
    ts2.append(t2)
    t2msts.append(t2mst)
    an3 = {}
    t3 = []
    for i in range(len(pairs)):
        an3_el, t3_el = compute_bsgt(graph=nx_graph.copy(), source=pairs[i][0], target=pairs[i][1])
        an3[i] = an3_el
        t3.append(t3_el)
    print("camerini DONE")
    t3 = sum(t3)
    ts3.append(t3)

    for key in an1.keys():
        print(pairs[key], an1[key])
    print(t1)
    print()
    for key in an2.keys():
        print(pairs[key], an2[key])
    print(t2)
    print()
    for key in an3.keys():
        print(pairs[key], an3[key])
    print(t3)
