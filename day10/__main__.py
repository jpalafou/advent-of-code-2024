class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, node, label=None):
        if node not in self.nodes:
            self.nodes[node] = {"label": label, "edges": []}

    def add_edge(self, node1, node2, label1=None, label2=None):
        self.add_node(node1, label1)
        self.add_node(node2, label2)
        self.nodes[node1]["edges"].append(node2)


def depth_first_search_for_label(graph, starting_node, label):
    visited = set()
    instances = 0

    def dfs(node):
        visited.add(node)
        for neighbour in graph.nodes[node]["edges"]:
            if neighbour not in visited:
                dfs(neighbour)
        if graph.nodes[node]["label"] == label:
            nonlocal instances
            instances += 1

    dfs(starting_node)
    return instances


def breadth_first_search_for_label(graph, starting_node, label):
    queue = [starting_node]
    instances = 0

    while queue:
        node = queue.pop()
        for neighbor in graph.nodes[node]["edges"]:
            queue.append(neighbor)
        if graph.nodes[node]["label"] == label:
            instances += 1

    return instances


# read map as array
with open("day10/input.txt") as f:
    _map = [[int(i) for i in line.strip()] for line in f]
    nrows, ncols = len(_map), len(_map[0])

# build graph of map positions
graph = Graph()
for i in range(nrows):
    for j in range(ncols):
        for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ni, nj = i + di, j + dj
            if 0 <= ni < nrows and 0 <= nj < ncols:
                if _map[ni][nj] - _map[i][j] == 1:
                    graph.add_edge((i, j), (ni, nj), _map[i][j], _map[ni][nj])

# compute the sum of the score of each trailhead
trailhead_score_sum = 0
trailhead_score_sum_paths = 0
for node in graph.nodes:
    if graph.nodes[node]["label"] == 0:
        trailhead_score_sum += depth_first_search_for_label(graph, node, 9)
        trailhead_score_sum_paths += breadth_first_search_for_label(graph, node, 9)

# print results
print("Part 1:", trailhead_score_sum)
print("Part 2:", trailhead_score_sum_paths)
