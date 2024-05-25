import networkx as nx
import time


def nlogn_median(l):
    l = sorted(l)
    if len(l) % 2 == 1:
        return l[int(len(l) // 2)]
    else:
        return l[int(len(l) // 2)]


def pick_pivot(l):
    assert len(l) > 0

    if len(l) < 5:
        return nlogn_median(l)
    chunks = chunked(l, 5)
    full_chunks = [chunk for chunk in chunks if len(chunk) == 5]
    sorted_groups = [sorted(chunk) for chunk in full_chunks]
    medians = [chunk[2] for chunk in sorted_groups]
    median_of_medians = quickselect_median(medians, pick_pivot)
    return median_of_medians

def chunked(l, chunk_size):
    return [l[i:i + chunk_size] for i in range(0, len(l), chunk_size)]



def quickselect_median(l, pivot_fn=pick_pivot):
    if len(l) % 2 == 1:
        return quickselect(l, int(len(l) // 2), pivot_fn)
    else:
        return int(0.5 * (quickselect(l, int(len(l)) // 2, pivot_fn) +
                      quickselect(l, int(len(l) // 2), pivot_fn)))


def quickselect(l, k, pivot_fn):
    if len(l) == 1:
        assert k == 0
        return l[0]

    pivot = pivot_fn(l)

    lows = [el for el in l if el < pivot]
    highs = [el for el in l if el > pivot]
    pivots = [el for el in l if el == pivot]

    if k < len(lows):
        return quickselect(lows, k, pivot_fn)
    elif k < len(lows) + len(pivots):
        return int(pivots[0])
    else:
        return quickselect(highs, k - len(lows) - len(pivots), pivot_fn)



def compute_bsgt(graph, source, target):
    time1 = time.time()
    b_st = 0
    while graph.number_of_edges() > 1 or b_st == 0:
        capacities = []
        for u, v in graph.edges():
            for key in graph[u][v].keys():
                capacities.append(graph[u][v][key]["capacity"])
        c_star = quickselect_median(capacities)
        count = 0
        edges_to_remove = []
        for u, v in graph.edges():
            for key in graph[u][v]:
                if graph[u][v][key]['capacity'] < c_star:
                    edges_to_remove.append((u, v, key))
                    count += 1
        if count == 0:
            break
        graph1 = graph.copy()
        graph1.remove_edges_from(edges_to_remove)
        

        if nx.has_path(graph1, source, target):
            b_st = c_star
            graph = graph1
        else:
            components = list(nx.connected_components(graph1))
            for component in range(len(components)):
                components[component] = tuple(components[component])
                t_node = -1                                         
                for node in range(1, len(components[component])):
                    if components[component][node] != target and components[component][node] != source:
                        nx.contracted_nodes(graph, components[component][0], components[component][node], self_loops=False, copy=False)
                    else:
                        t_node = components[component][node]
                if t_node != -1:
                    nx.contracted_nodes(graph, t_node, components[component][0], self_loops=False, copy=False)
    time2 = time.time()
    return b_st, time2 - time1


if __name__ == '__main__':
    G = nx.Graph()
    G.add_edge('s', 'a', capacity=3)
    G.add_edge('s', 'b', capacity=2)
    G.add_edge('a', 't', capacity=4)
    G.add_edge('b', 't', capacity=5)

    source = 's'
    target = 't'

    result, t = compute_bsgt(G, source, target)
    print(result)