def find_guard(_map):
    for i, row in enumerate(_map):
        for j, char in enumerate(row):
            if char == "^":
                return (i, j), (-1, 0)
            elif char not in ".#":
                raise ValueError(f"Unknown character {char}")
    raise ValueError("No guard found")


def next_pos(pos, direction):
    return (pos[0] + direction[0], pos[1] + direction[1])


def rotate_clockwise(direction):
    return (direction[1], -direction[0])


def evolve_guard(_map):
    pos, direction = find_guard(_map)
    path = []

    while True:
        if pos not in path:
            path.append(pos)
        _pos = next_pos(pos, direction)
        if not (0 <= _pos[0] < len(_map) and 0 <= _pos[1] < len(_map[0])):
            break
        if _map[_pos[0]][_pos[1]] == "#":
            direction = rotate_clockwise(direction)
            _pos = next_pos(pos, direction)
        pos = _pos

    return path


# read the map
with open("day06/input.txt") as f:
    _map = f.read().split("\n")

# print the unique number of positions visited by the guard
print("Part 1:", len(evolve_guard(_map)))
