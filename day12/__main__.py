from itertools import product


class UndirectedGraph:
    def __init__(self):
        self.nodes = {}

    def __getitem__(self, node):
        return self.nodes[node]

    def add_node(self, node, label=None):
        if node not in self.nodes:
            self.nodes[node] = {"edges": set(), "label": label}

    def add_edge(self, node1, node2, label1=None, label2=None):
        self.add_node(node1, label1)
        self.add_node(node2, label2)
        self.nodes[node1]["edges"].add(node2)
        self.nodes[node2]["edges"].add(node1)

    def remove_node(self, node):
        for neighbor in self.nodes[node]["edges"]:
            self.nodes[neighbor]["edges"].remove(node)
        del self.nodes[node]


# read map as array
with open("day12/input.txt") as f:
    _map = [line.strip() for line in f.readlines()]
    nrows, ncols = len(_map), len(_map[0])

# build graph of map positions
garden = UndirectedGraph()
for i, j in product(range(nrows), range(ncols)):
    for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        ni, nj = i + di, j + dj
        if 0 <= ni < nrows and 0 <= nj < ncols:
            garden.add_edge((i, j), (ni, nj), _map[i][j], _map[ni][nj])


def simplify_fence(fence):
    for node in set(fence.nodes.keys()):
        if len(fence[node]["edges"]) == 2:
            lnode, rnode = fence[node]["edges"]
            lmode = "-" if lnode[0] == node[0] else "|"
            rmode = "-" if rnode[0] == node[0] else "|"
            if lmode == rmode:
                fence.remove_node(node)
                fence.add_edge(lnode, rnode)


def compute_fence_cost(garden, nrows, ncols, bulk_pricing):
    visited = set()
    cost = 0

    # breadth-first search to find all like connected components and place fences
    def search_plot_interior(starting_node):
        queue = {starting_node}
        area = 0
        fence = UndirectedGraph()

        while queue:
            node = queue.pop()
            visited.add(node)
            area += 1

            for direction in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                neighbor = (node[0] + direction[0], node[1] + direction[1])
                if neighbor in garden[node]["edges"]:
                    if garden[neighbor]["label"] == garden[starting_node]["label"]:
                        if neighbor not in visited:
                            queue.add(neighbor)
                        continue
                if direction[0] == 0:
                    j = max(node[1], neighbor[1])
                    fencepost1, fencepost2 = (node[0], j), (node[0] + 1, j)
                elif direction[1] == 0:
                    i = max(node[0], neighbor[0])
                    fencepost1, fencepost2 = (i, node[1]), (i, node[1] + 1)
                fence.add_edge(fencepost1, fencepost2)

        return area, fence

    for i, j in product(range(nrows), range(ncols)):
        if (i, j) not in visited:
            area, fence = search_plot_interior((i, j))
            if bulk_pricing:
                simplify_fence(fence)
            edges = set()
            for node1 in fence.nodes.keys():
                for node2 in fence[node1]["edges"]:
                    edges.add(tuple(sorted((node1, node2))))
            cost += area * len(edges)
    return cost


# print cost of fences between the distinct garden regions
print("Part 1:", compute_fence_cost(garden, nrows, ncols, False))
print("Part 2:", compute_fence_cost(garden, nrows, ncols, True))
