from itertools import combinations


def find_antennae(_map):
    nrows, ncols = len(_map), len(_map[0])
    locations = {}
    for i in range(nrows):
        for j in range(ncols):
            frequency = _map[i][j]
            if frequency == ".":
                continue
            if frequency not in locations:
                locations[frequency] = []
            locations[frequency].append((i, j))
    return locations


def is_in_map(_map, pos):
    return 0 <= pos[0] < len(_map) and 0 <= pos[1] < len(_map[0])


def _extrapolate_to_antinode(pos1, pos2):
    drow, dcol = pos2[0] - pos1[0], pos2[1] - pos1[1]
    return pos2[0] + drow, pos2[1] + dcol


def extrapolate_to_antinotes(_map, pos1, pos2):
    antinodes = [
        _extrapolate_to_antinode(pos1, pos2),
        _extrapolate_to_antinode(pos2, pos1),
    ]
    return [node for node in antinodes if is_in_map(_map, node)]


def extrapolate_to_harmonic_antinotes(_map, pos1, pos2):
    antinodes = [pos1, pos2]
    while True:
        next_antinode = _extrapolate_to_antinode(antinodes[-2], antinodes[-1])
        if is_in_map(_map, next_antinode):
            antinodes.append(next_antinode)
        else:
            break
    while True:
        next_antinode = _extrapolate_to_antinode(antinodes[1], antinodes[0])
        if is_in_map(_map, next_antinode):
            antinodes.insert(0, next_antinode)
        else:
            break
    return antinodes


def count_unique_antinode_locations(_map, harmonic=False):
    antennae = find_antennae(_map)
    antinode_locations = set()
    for antenna_locations in antennae.values():
        for pos1, pos2 in combinations(antenna_locations, 2):
            for node in {
                False: extrapolate_to_antinotes,
                True: extrapolate_to_harmonic_antinotes,
            }[harmonic](_map, pos1, pos2):
                antinode_locations.add(node)
    return len(antinode_locations)


# read map
with open("day08/input.txt") as f:
    _map = list(f.read().split("\n"))

# print number of unique antinode locations with and without harmonic extrapolation
print("Part 1:", count_unique_antinode_locations(_map))
print("Part 1:", count_unique_antinode_locations(_map, harmonic=True))
