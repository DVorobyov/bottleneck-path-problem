try:
    from FibHeap import FibHeapForPrims
except ImportError:
    from .FibHeap import FibHeapForPrims

def prims_mst(grf):
	precursor = [None] * grf.nfverts
	visited = set()

	src = 0
	heap = FibHeapForPrims(grf.nfverts)

	for _ in range(grf.nfverts):
		u = heap.extract_min()
		visited.add(u)

		for v, cur_key in grf.graph[u].items():
			if v not in visited and cur_key > heap.fetch_key(v):
				heap.decrease_key(v, cur_key)
				precursor[v] = u

	return precursor