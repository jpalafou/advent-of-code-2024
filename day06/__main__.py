# read the map
with open("day06/input.txt") as f:
    row_map = list(f.read().split("\n"))
col_map = [
    "".join([row_map[i][j] for i in range(len(row_map))])
    for j in range(len(row_map[0]))
]


def find_guard(row_map):
    for i, row in enumerate(row_map):
        for j, char in enumerate(row):
            if char == "^":
                return (i, j)


def move_guard(pos, r, steps=1):
    i, j = pos
    if r == 0:
        return (i, j + steps)
    elif r == 1:
        return (i - steps, j)
    elif r == 2:
        return (i, j - steps)
    elif r == 3:
        return (i + steps, j)


def evolve_guard(row_map, col_map):
    pos, r = find_guard(row_map), 1
    visited = set()
    free = False

    while not free:
        # find line of sight
        if r == 0:
            line_of_sight = row_map[pos[0]][slice(pos[1] + 1, None)]
        elif r == 1:
            line_of_sight = col_map[pos[1]][slice(pos[0] - 1, None, -1)]
        elif r == 2:
            line_of_sight = row_map[pos[0]][slice(pos[1] - 1, None, -1)]
        elif r == 3:
            line_of_sight = col_map[pos[1]][slice(pos[0] + 1, None)]

        # determine if there is an obstacle in the line of sight
        if "#" in line_of_sight:
            n_steps = line_of_sight.index("#")
        else:
            n_steps = len(line_of_sight)
            free = True

        # update visited set. if there is a cycle, return "cycle"
        for i in range(n_steps + 1):
            _pos = move_guard(pos, r, i)
            if (_pos, r) in visited:
                return "cycle"
            visited.add((_pos, r))

        # update position and direction
        pos = move_guard(pos, r, n_steps)
        if not free:
            r = (r - 1) % 4

    return {pos for pos, _ in visited}


# count positions visited by guard
visited_positions = evolve_guard(row_map, col_map)
print("Part 1:", len(visited_positions))


def place_obstacle(row_map, col_map, pos):
    _row_map, _col_map = row_map.copy(), col_map.copy()
    _row_map[pos[0]] = (
        row_map[pos[0]][: pos[1]] + "#" + row_map[pos[0]][slice(pos[1] + 1, None)]
    )
    _col_map[pos[1]] = (
        col_map[pos[1]][: pos[0]] + "#" + col_map[pos[1]][slice(pos[0] + 1, None)]
    )
    return _row_map, _col_map


# place obstacles and check if they produce a cycle
possible_loops = 0
for pos in visited_positions:
    if row_map[pos[0]][pos[1]] in "#^":
        continue
    _row_map, _col_map = place_obstacle(row_map, col_map, pos)
    if evolve_guard(_row_map, _col_map) == "cycle":
        possible_loops += 1
print("Part 2:", possible_loops)
