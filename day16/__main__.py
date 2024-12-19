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
    return free_space, starting_pos, target_pos


def find_cheapest_maze_path(free_space, starting_pos, target_pos):
    next_pos = ((0, 1), (-1, 0), (0, -1), (1, 0))  # indexed by r

    # breadth first search for cheapest maze path
    queue = {((starting_pos,), 0, 0)}  # (path, r, cost)
    cheapest_cost = None

    while queue:
        path, r, cost = queue.pop()
        pos = path[-1]

        if target_pos in path and (cheapest_cost is None or cost < cheapest_cost):
            cheapest_cost = cost

        for dr in [-1, 0, 1]:
            _r = (r + dr) % 4
            _pos = (
                (pos[0] + next_pos[r][0], pos[1] + next_pos[r][1]) if dr == 0 else pos
            )
            if _pos in free_space and _pos not in path[:-1]:
                queue.add((path + (_pos,), _r, cost + 1000 * abs(dr) + (_pos != pos)))

    return cheapest_cost


# print cheapest path cost
print("Part 1:", find_cheapest_maze_path(*read_maze("day16/input.txt")))
