from itertools import product

import matplotlib.pyplot as plt
import numpy as np


def find_longest_path(undirected_graph):

    def dfs(node, visited, depth=0):
        visited.add(node)
        farthest_node, max_depth = node, depth
        for neighbor in undirected_graph[node]:
            if neighbor not in visited:
                new_node, new_depth = dfs(neighbor, visited, depth + 1)
                if new_depth > max_depth:
                    farthest_node, max_depth = new_node, new_depth
        return farthest_node, max_depth

    max_path = (None, 0)
    for node in undirected_graph:
        new_path = dfs(node, set())
        max_path = new_path if new_path[1] > max_path[1] else max_path
    return max_path


def write_frame_to_file(robot_states, nrows, ncols, t=None):
    rows = ["." * ncols for _ in range(nrows)]
    for state in robot_states:
        x, y = state[:2]
        rows[y] = rows[y][slice(None, x)] + "#" + rows[y][slice(x + 1, None)]
    with open(f"day14/frames/frame_{t:02d}.txt", "w") as f:
        for row in rows:
            f.write(row + "\n")


def step(robot_states, nrows=103, ncols=101, t=None):
    out = robot_states
    out[:, :2] = out[:, :2] + out[:, 2:]
    out[:, :2] = np.mod(out[:, :2], [ncols, nrows])
    if t is not None:
        write_frame_to_file(out, nrows, ncols, t + 1)
    return out


def get_safety_factor(robot_states, nrows, ncols):
    array = np.zeros((nrows, ncols), dtype=int)
    for state in robot_states:
        array[state[1], state[0]] += 1
    quadrant_slices = product(
        [slice(None, nrows // 2), slice(None, -nrows // 2, -1)],
        [slice(None, ncols // 2), slice(None, -ncols // 2, -1)],
    )
    return np.prod([np.sum(array[q]) for q in quadrant_slices])


# read the robot states
with open("day14/input.txt") as f:
    robot_states = []
    for line in f:
        state = [
            int(x)
            for x in line.strip()
            .replace("p=", "")
            .replace("v=", "")
            .replace(" ", ",")
            .split(",")
        ]
        robot_states.append(state)
    robot_states = np.array(robot_states)

# set map shape
nrows, ncols = 103, 101

# evolve to 10000 seconds and plot the longest path to try to find when the egg appears
longest_paths = []
for t in range(0, 10000):
    robot_states = step(robot_states, nrows, ncols, t)

    if t + 1 == 100:
        # print the safety factor
        print("Part 1:", get_safety_factor(robot_states, nrows, ncols))

    # form graph of adjacent robots. save the longest path length
    undirected_graph = {}
    for state in robot_states:
        node = tuple([int(x) for x in tuple(state[:2])])
        if node not in undirected_graph:
            undirected_graph[node] = set()
        for d in product([-1, 0, 1], repeat=2):
            neighbor = node[0] + d[0], node[1] + d[1]
            if d != (0, 0) and neighbor in undirected_graph:
                undirected_graph[node].add(neighbor)
                undirected_graph[neighbor].add(node)
    longest_paths.append(find_longest_path(undirected_graph)[1])

# plot number of edges at each time and show that there is a peak in connectivity
plt.plot(longest_paths)
plt.show()
