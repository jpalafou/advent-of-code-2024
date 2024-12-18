def read_positions_and_instructions(file, double_wide=False):
    boxes = set()
    obstacles = set()
    robot = None
    instructions = ""

    # read the box, obstacle, and robot positions and the instructions from file
    with open("day15/input.txt") as f:
        for i, line in enumerate(f):
            if line.strip() == "":
                break
            for j, c in enumerate(line.strip()):
                pos = (i, 2 * j if double_wide else j)
                if c == "O":
                    boxes.add(pos)
                elif c == "#":
                    obstacles.add(pos)
                elif c == "@":
                    robot = pos
        for line in f:
            instructions += line.strip()
    return boxes, obstacles, robot, instructions


def compute_box_coordinate_sum(boxes):
    return sum(100 * box[0] + box[1] for box in list(boxes))


def simulate(boxes, obstacles, inital_robot_position, instructions, double_wide=False):
    unit_directions = {">": [(0, 1)], "^": [(-1, 0)], "<": [(0, -1)], "v": [(1, 0)]}
    from_robot_search_directions = (
        {
            ">": [(0, 1)],
            "^": [(-1, -1), (-1, 0)],
            "<": [(0, -2)],
            "v": [(1, -1), (1, 0)],
        }
        if double_wide
        else unit_directions
    )
    from_box_search_directions = (
        {
            ">": [(0, 2)],
            "^": [(-1, -1), (-1, 0), (-1, 1)],
            "<": [(0, -2)],
            "v": [(1, -1), (1, 0), (1, 1)],
        }
        if double_wide
        else unit_directions
    )
    pos = inital_robot_position

    for c in instructions:
        # breadth first search for boxes that interact with the robot
        movable_boxes = []
        queue = {
            (pos[0] + _d1, pos[1] + _d2) for _d1, _d2 in from_robot_search_directions[c]
        }
        space = True

        while queue:
            _pos = queue.pop()
            if _pos in boxes:
                movable_boxes.append(_pos)
                for _d1, _d2 in from_box_search_directions[c]:
                    queue.add((_pos[0] + _d1, _pos[1] + _d2))
                continue
            elif _pos in obstacles:
                space = False
                break
        if space:
            # if there is room, move all the boxes and the robot
            boxes -= set(movable_boxes)
            d1, d2 = unit_directions[c][0]
            boxes.update({(box[0] + d1, box[1] + d2) for box in movable_boxes})
            pos = (pos[0] + d1, pos[1] + d2)

    return compute_box_coordinate_sum(boxes)


# print the sum of the coordinates of the boxes after following the instructions
file = "day15/input.txt"
print(
    "Part 1:",
    simulate(*read_positions_and_instructions(file)),
)
print(
    "Part 2:",
    simulate(*read_positions_and_instructions(file, True), True),
)
