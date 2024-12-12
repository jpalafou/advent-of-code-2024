def parse_disk(disk_map, as_blocks=False):
    layout = {}
    idx = 0
    for i, count in enumerate(disk_map):
        value = i // 2 if i % 2 == 0 else None
        if as_blocks or i % 2 != 0:
            layout[idx] = (value, count)
            idx += count
        else:
            for _ in range(count):
                layout[idx] = (value, 1)
                idx += 1
    return layout


def checksum(layout):
    out = 0
    for i in sorted(layout.keys()):
        value, block_size = layout[i]
        if value is None:
            continue
        for _i in range(block_size):
            out += value * (i + _i)
    return out


def compress(layout, as_blocks=False):
    layout = layout.copy()
    no_space_before_this_idx = 0
    for i in range(sum([v[1] for v in layout.values()]) - 1, -1, -1):
        if i not in layout or layout[i][0] is None:
            continue
        value, block_size = layout[i]
        for j in range(no_space_before_this_idx, i):
            if j not in layout or layout[j][0] is not None:
                continue
            is_none, _block_size = layout[j]
            if not as_blocks:
                no_space_before_this_idx = j
            if _block_size >= block_size:
                layout[j] = (value, block_size)
                layout[i] = (None, block_size)
                if _block_size > block_size:
                    layout[j + block_size] = (None, _block_size - block_size)
                break
    return layout


# read disk map
with open("day09/input.txt") as f:
    dm = [int(i) for i in f.readline().strip()]

# move memory blocks to empty slots then calculate checksum
print("Part 1:", checksum(compress(parse_disk(dm))))
print("Part 2:", checksum(compress(parse_disk(dm, as_blocks=True), as_blocks=True)))
