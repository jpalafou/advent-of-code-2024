def build_graph(edges):
    graph = {}
    for n1, n2 in edges:
        if n1 not in graph:
            graph[n1] = []
        if n2 not in graph:
            graph[n2] = []
        graph[n1].append(n2)
    return graph


def depth_first_search_topological_sort(graph, starting_node):
    visited = set()
    stack = []

    def dfs(node):
        visited.add(node)
        for neighbour in graph[node]:
            if neighbour not in visited:
                dfs(neighbour)
        stack.append(node)

    dfs(starting_node)
    return stack[::-1]


def filter_rules_by_update(rules, update):
    return [rule for rule in rules if rule[0] in update and rule[1] in update]


# read data
with open("day05/input.txt") as f:
    rules = [[int(n) for n in line.strip().split("|")] for line in f if "|" in line]
with open("day05/input.txt") as f:
    updates = [[int(i) for i in line.strip().split(",")] for line in f if "," in line]

# compute some of middle page numbers of valid and corrected updates
sum_of_valid_update_centers, sum_of_corrected_update_centers = 0, 0
for update in updates:
    # build graph from relevant rules
    graph = build_graph(filter_rules_by_update(rules, update))

    # find root node
    root_nodes = set(graph.keys()) - {
        node for neighbours in graph.values() for node in neighbours
    }
    if len(root_nodes) != 1:
        raise ValueError("Multiple root nodes found")
    root_node = root_nodes.pop()

    # sort graph topologically
    sorted_update = depth_first_search_topological_sort(graph, root_node)

    # add middle page number accordingly
    if update == sorted_update:
        sum_of_valid_update_centers += update[len(update) // 2]
    else:
        sum_of_corrected_update_centers += sorted_update[len(update) // 2]

# print results for both cases
print("Part 1:", sum_of_valid_update_centers)
print("Part 2:", sum_of_corrected_update_centers)
