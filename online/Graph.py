from collections import defaultdict

class Graph:
	def __init__(self, nfverts = None, graph = None, representation = None):
		self.nfverts = nfverts

		self.representation = representation if representation else "matrix"
		if self.representation == "matrix" and graph is None:
			self.graph = []

		elif self.representation == "lists" and graph is None:
			self.graph = defaultdict(dict)
		
		elif self.representation == "lists" and graph is not None:
			self.graph = graph
		
		else:
			raise ValueError("Invalid representation.")

	def read_from_file(self, input_file): 
		self.nfverts = int(input_file.readline())
		
		if self.representation == "matrix": 
			def inner_loop(u):
				self.graph.append([int(number) for number in input_file.readline().split()])
		else:
			def inner_loop(u):
				for v, number in enumerate(input_file.readline().split()):
					number = int(number)
					if number != 0: self.graph[u][v] = number


		for u in range(self.nfverts): 
			inner_loop(u)

	def matrix_to_lists(self):
		if self.representation == "matrix":
			adj_lists = defaultdict(dict)
			for i, row in enumerate(self.graph):
				for j, ele in enumerate(row):
					if ele != 0: adj_lists[i][j] = ele
			self.graph = adj_lists
			self.representation = "lists"

	def lists_to_matrix(self):
		if self.representation == "lists":
			adj_mat = []
			for i in range(self.nfverts):
				row = []
				for j in range(self.nfverts):
					try:
						ele = self.graph[i][j]
					except KeyError:
						ele = 0
					row.append(ele)
				adj_mat.append(row)
	
			self.graph = adj_mat
			self.representation = "matrix"

	def fill_with_zeros(self):
		assert self.representation == "matrix", "Wrong representation!"
		self.graph = [[0] * self.nfverts for _ in range(self.nfverts)]

	def __str__(self):
		if self.representation == "matrix":
			return "\n".join(str(row) for row in self.graph)
			return '\n'.join(str(adj_list) for adj_list in self.graph.items())

def compute_mst_and_cost(precursor, grf):
	mst = Graph(grf.nfverts, representation = "lists")
	cost = 0
	for cur, parent in enumerate(precursor[1:], 1):
		mst.graph[parent][cur] = grf.graph[parent][cur]
		mst.graph[cur][parent] = grf.graph[parent][cur]
		cost += grf.graph[parent][cur]
	
	return mst, cost