def rec_det(A):
    return A[0][0] * A[1][1] - A[0][1] * A[1][0]


def det_times_inv(A):
    return [[A[1][1], -A[0][1]], [-A[1][0], A[0][0]]]


def mat_mul(A, x):
    return A[0][0] * x[0] + A[0][1] * x[1], A[1][0] * x[0] + A[1][1] * x[1]


class GameMachine:
    def __init__(self, button_A, button_B):
        self.buttons = [[button_A[0], button_B[0]], [button_A[1], button_B[1]]]

    def inverse_button_press(self, pos):
        _rec_det = rec_det(self.buttons)
        if _rec_det == 0:
            # for some reason, each game machine has only one winning path
            raise ValueError("The buttons are not invertible")
        x1, x2 = mat_mul(det_times_inv(self.buttons), pos)
        if x1 % _rec_det != 0 or x2 % _rec_det != 0:
            return None
        return (x1 // _rec_det, x2 // _rec_det)


def load_game_machines(file, long_mode=False):
    # read the file and parse the game machines and their prizes
    game_machines = []
    with open(file) as f:
        buttons = {}
        for line in f.readlines():
            _line = line.strip()
            if _line.startswith("Button A") or _line.startswith("Button B"):
                buttons[_line[7]] = tuple(
                    [
                        int(x)
                        for x in _line.strip(f"{_line[:8]}: X+")
                        .replace("Y+", "")
                        .split(", ")
                    ]
                )
                continue
            if _line.startswith("Prize"):
                prize = tuple(
                    [
                        int(x)
                        for x in _line.strip("Prize: X=").replace("Y=", "").split(", ")
                    ]
                )
                game_machines.append(
                    (
                        GameMachine(buttons["A"], buttons["B"]),
                        (
                            (prize[0] + 10000000000000, prize[1] + 10000000000000)
                            if long_mode
                            else prize
                        ),
                    )
                )
    return game_machines


def compute_cost(game_machines):
    cost = 0
    for i in range(len(game_machines)):
        gm, prize = game_machines[i]
        cheapest_path = gm.inverse_button_press(prize)
        if cheapest_path is not None:
            cost += 3 * cheapest_path[0] + cheapest_path[1]
    return cost


# print the result for normal and long game modes
file = "day13/input.txt"
print("Part 1:", compute_cost(load_game_machines(file)))
print("Part 2:", compute_cost(load_game_machines(file, True)))
