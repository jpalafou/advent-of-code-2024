import sys


class Graph:
    def __init__(self):
        self.weights = {}

    def add_node(self, node):
        if node not in self.weights:
            self.weights[node] = {}

    def add_edge(self, node1, node2, weight):
        self.add_node(node1)
        self.add_node(node2)
        self.weights[node1][node2] = weight


def rotate_unit_vector(u, r=1):
    if r == 1:
        return -u[1], u[0]
    if r == 0:
        return u
    if r < 0:
        return rotate_unit_vector(u, r % 4)
    return rotate_unit_vector(rotate_unit_vector(u, r - 1))


def read_maze(file):
    # read free space, starting, and target positions from file
    free_space = set()
    starting_pos = None
    target_pos = None
    with open(file) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.strip()):
                pos = (i, j)
                if c in ".SE":
                    free_space.add(pos)
                if c == "S":
                    starting_pos = pos
                elif c == "E":
                    target_pos = pos

    # build directed graph with bfs
    visited = set()
    queue = {(starting_pos, 0)}
    graph = Graph()
    while queue:
        pos, r = queue.pop()
        visited.add((pos, r))
        for dr in [-1, 0, 1]:
            _r = (r + dr) % 4
            direction = rotate_unit_vector((0, 1), _r)
            _pos = pos[0] + direction[0], pos[1] + direction[1]
            if _pos in free_space:
                graph.add_edge((pos, r), (_pos, _r), 1 + 1000 * abs(dr))
                if (_pos, _r) not in visited and _pos != target_pos:
                    queue.add((_pos, _r))

    return graph, starting_pos, target_pos


def find_cheapest_maze_path(graph, starting_pos, target_pos):
    # Dijkstra search for cheapest maze path
    distance = {}
    previous = {}
    queue = set()
    for node in graph.weights:
        distance[node] = sys.maxsize
        previous[node] = None
        queue.add(node)
    distance[(starting_pos, 0)] = 0

    while queue:
        node = min(queue, key=lambda x: distance[x])
        queue.remove(node)

        for neighbor, weight in graph.weights[node].items():
            alt = distance[node] + weight
            if neighbor in queue and alt < distance[neighbor]:
                distance[neighbor] = alt
                previous[neighbor] = node

    cheapest_path = min(
        distance[(target_pos, r)] for r in range(4) if (target_pos, r) in graph.weights
    )
    return cheapest_path


# print length of cheapest path
print("Part 1:", find_cheapest_maze_path(*read_maze("day16/input.txt")))
