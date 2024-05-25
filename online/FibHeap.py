from collections import defaultdict
INFINITY = float('inf')


class FibHeapNode:
	def __init__(self, ele):
		self.ele = ele
		self.rank = 0

		self.parent = None
		self.left = self
		self.right = self
		self.child = None

		self.mark = False

	def children_generator(self):
		if self.child is None: return 
		
		cur_child = self.child
		
		while cur_child.right is not self.child:
			yield cur_child
			cur_child = cur_child.right
		yield cur_child

	def print_tree(self, tabwidth = 0):
		print(tabwidth*"    ", self.ele, '*' if self.mark else '', sep = "")
		for childtree in self.children_generator():
			childtree.print_tree(tabwidth + 1)

	def __str__(self):
		return str(self.ele)

	def __lt__(self, other): return self.ele < other.ele
	def __le__(self, other): return self.ele <= other.ele
	def __gt__(self, other): return self.ele > other.ele
	def __ge__(self, other): return self.ele >= other.ele
	def __eq__(self, other): return self.ele == other.ele


class FibHeap:
	def __init__(self, head = None, min_node = None):
		if head is None:
			self.head = None
			self.min_node = None

		else:
			self.head = head
			self.min_node = min_node
		self.Node = FibHeapNode

	def merge(self, other):
		if self.head is None:
			self.head = other.head
			return
		elif other.head is None:
			return

		self.min_node = max(self.min_node, other.min_node)
		self.head = self._merge_lls(self.head, other.head)

		other.head = None
		other.min_node = None

	def __link(self, node1, node2):
		node2.parent = node1
		node2.mark = False
		node1.rank += 1
		if node1.child:
			head = node1.child
			tail = head.left
			self.__attach(node2, head)
			self.__attach(tail, node2)

		else:
			node1.child = node2

	def __root_list_generator(self):
		if self.head is None: return
		cur_node = self.head.right

		while cur_node is not self.head:
			yield cur_node.left
			cur_node = cur_node.right

		yield cur_node.left

	def print_heap(self):
		print(f"### head = {self.head}, min_node = {self.min_node} ###")
		for root in self.__root_list_generator():
			root.print_tree()
		print()

	def _remove_node(self, node):
		if node is node.right:
			self.head = None
			return

		if self.head is node:
			self.head = self.head.right

		self.__attach(node.left, node.right)
		node.left, node.right = node, node

	def _consolidate(self):		
		self.degree_tree_map = defaultdict(lambda: None)

		def merging_trees(cur_root):
			other_root = self.degree_tree_map[cur_root.rank]


			if other_root is None:
				self.degree_tree_map[cur_root.rank] = cur_root
				return
			else:
				self.degree_tree_map[cur_root.rank] = None
				if cur_root >= other_root:
					self._remove_node(other_root)
					self.__link(cur_root, other_root) 
					combined_root = cur_root
				else:
					self._remove_node(cur_root)
					self.__link(other_root, cur_root) 
					combined_root = other_root

				merging_trees(combined_root)

		for cur_root in self.__root_list_generator():
			merging_trees(cur_root)
		try:
			roots_iter = filter(lambda node: node is not None, self.degree_tree_map.values())
			self.min_node = max(roots_iter) 
		except ValueError as err:
			if str(err) == "max() arg is an empty sequence":
				self.min_node = None
			else: 
				raise ValueError(err)

	def __attach(self, node1, node2):
		node1.right = node2
		node2.left = node1

	def _merge_lls(self, head_one, head_two):
		tail_one, tail_two = head_one.left, head_two.left
		self.__attach(tail_one, head_two)
		self.__attach(tail_two, head_one)
		return head_one

	def extract_min(self):
		if not self.head: 
			raise IndexError("Popping from an empty heap.")

		node_to_be_popped = self.min_node

		if node_to_be_popped.child: 
			self._merge_lls(self.head, node_to_be_popped.child)

		self._remove_node(node_to_be_popped)

		self._consolidate()

		temp = node_to_be_popped.ele
		node_to_be_popped.ele = None
		return temp

	def __cut(self, node):
		if node is node.right:
			node.parent.child = None
			
		else:
			if node.parent.child is node: 
				node.parent.child = node.parent.child.right

			self.__attach(node.left, node.right)

			node.left, node.right = node, node
	
		node.parent.rank -= 1
		node.parent = None			

		self.__insert_node(node) 

	def __cascading_cut(self, node):
		if node.parent is None or node.parent.ele is None:
			pass

		else:
			if node.mark:
				parent = node.parent
				self.__cut(node)
				self.__cascading_cut(parent)
			else:
				node.mark = True

	def decrease_key(self, node, new_ele):
		if node.ele > new_ele:
			raise ValueError("new_ele is lower than node's current ele.")

		node.ele = new_ele

		if node.parent is None or node.parent.ele is None:
			if self.min_node < node:
				self.min_node = node
			return

		elif node <= node.parent:
			pass
		else:
			parent = node.parent
			self.__cut(node)
			self.__cascading_cut(parent)

	def __insert_node(self, new_node):
		
		if self.head:
			self._merge_lls(self.head, new_node)

			if new_node > self.min_node: self.min_node = new_node

		else: 
			self.head = new_node
			self.min_node = new_node

	def insert(self, new_ele):
		new_node = self.Node(new_ele)
		self.__insert_node(new_node)

class FibHeapNodeForPrims(FibHeapNode):
	def __init__(self, vertex, ele):
		super().__init__(ele)
		self.vertex = vertex

	def __str__(self):
		return str((self.vertex, self.ele))

	def print_tree(self, tabwidth = 0):
		print(tabwidth*"    ", self.vertex, ':', self.ele, '*' if self.mark else '', sep = "")
		for childtree in self.children_generator():
			childtree.print_tree(tabwidth + 1)



class FibHeapForPrims(FibHeap):
	def __init__(self, nfverts):
		self.Node = FibHeapNodeForPrims

		src = 0 
		self.vertex_heapnode_map = []

		head = self.Node(src, 0)
		tail = head
		self.vertex_heapnode_map.append(head)

		for vx in range(1, nfverts):
			node = self.Node(vx, -INFINITY)
			self.vertex_heapnode_map.append(node)
			
			tail.right = node
			node.left = tail
			tail = node

		tail.right = head
		head.left = tail

		self.head = self.min_node = head

	def extract_min(self):
		if not self.head: 
			raise IndexError("Popping from an empty heap.")

		node_to_be_popped = self.min_node

		if node_to_be_popped.child:
			self._merge_lls(self.head, node_to_be_popped.child)

		self._remove_node(node_to_be_popped)

		self._consolidate()

		node_to_be_popped.ele = None
		return node_to_be_popped.vertex


	def decrease_key(self, vertex, new_key):
		node = self.vertex_heapnode_map[vertex]
		super().decrease_key(node, new_key)

	def fetch_key(self, vertex):
		return self.vertex_heapnode_map[vertex].ele