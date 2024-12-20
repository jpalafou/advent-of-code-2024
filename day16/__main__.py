from collections import deque
from sys import maxsize


def rotate_unit_vector(u, r=1):
    if r == 1:
        return -u[1], u[0]
    if r == 0:
        return u
    return rotate_unit_vector(rotate_unit_vector(u, r - 1))


def read_maze(file):
    # read free space, starting, and target positions from file
    free_space = set()
    with open(file) as f:
        for i, line in enumerate(f.readlines()):
            for j, c in enumerate(line.strip()):
                if c in ".SE":
                    free_space.add((i, j))
                if c == "S":
                    starting_pos = (i, j)
                elif c == "E":
                    target_pos = (i, j)

    # define starting node
    starting_node = (starting_pos, 0)

    # build directed graph with bfs
    visited = set()
    queue = {starting_node}
    graph = {}
    while queue:
        pos, r = queue.pop()
        visited.add((pos, r))
        for dr in [-1, 0, 1]:
            _r = (r + dr) % 4
            direction = rotate_unit_vector((0, 1), _r)
            _pos = pos[0] + direction[0], pos[1] + direction[1]
            if _pos in free_space:
                # add edge
                if (pos, r) not in graph:
                    graph[(pos, r)] = {}
                if (_pos, _r) not in graph:
                    graph[(_pos, _r)] = {}
                graph[(pos, r)][(_pos, _r)] = 1 + 1000 * abs(dr)

                # update queue
                if (_pos, _r) not in visited and _pos != target_pos:
                    queue.add((_pos, _r))

    # define target nodes
    target_nodes = [node for node in graph if node[0] == target_pos]

    return graph, starting_node, target_nodes


def find_cheapest_maze_path(graph, starting_node, target_nodes):
    # bfs search for cheapest paths
    distance = {node: maxsize for node in graph}
    distance[starting_node] = 0
    previous = {node: [] for node in graph}
    queue = deque(graph.keys())
    queue.appendleft(starting_node)

    while queue:
        node = queue.popleft()

        for neighbor, weight in graph[node].items():
            alt = distance[node] + weight
            if alt < distance[neighbor]:
                distance[neighbor] = alt
                previous[neighbor].clear()
                queue.append(neighbor)
            if alt <= distance[neighbor]:
                previous[neighbor].append(node)

    # find cheapest path cost and gather all the positions on a cheapest path
    shortest_distance = min(distance[node] for node in target_nodes)
    visited_pos = set()
    for target_node in target_nodes:
        if distance[target_node] == shortest_distance:
            queue = {target_node}
            while queue:
                node = queue.pop()
                visited_pos.add(node[0])
                for parent in previous[node]:
                    queue.add(parent)

    return shortest_distance, len(visited_pos)


# print cost of cheapest path and the number of visited positions
lowest_path_cost, visited_pos = find_cheapest_maze_path(*read_maze("day16/input.txt"))
print("Part 1:", lowest_path_cost, "\nPart 2:", visited_pos)
