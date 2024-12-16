from itertools import product


class GameMachine:
    def __init__(self, button_A, button_B, prize):
        self.buttons = {"A": button_A, "B": button_B}
        self.prize = prize
        self.reset()

    def press_button(self, button, times=1):
        self.tokens += {"A": 3, "B": 1}[button] * times
        _button = self.buttons[button]
        self.pos = (self.pos[0] + _button[0] * times, self.pos[1] + _button[1] * times)
        if self.pos == self.prize:
            self.found_prize = True
        elif self.pos[0] > self.prize[0] or self.pos[1] > self.prize[1]:
            self.overshot_prize = True

    def reset(self):
        self.pos = (0, 0)
        self.tokens = 0
        self.found_prize = False
        self.overshot_prize = False


def find_cheapest_path(game_machine):
    cheapest_path = (None, None, None)
    for a_times, b_times in product(range(1, 101), repeat=2):
        game_machine.reset()
        game_machine.press_button("A", a_times)
        game_machine.press_button("B", b_times)
        if game_machine.found_prize:
            if cheapest_path[2] is None or game_machine.tokens < cheapest_path[2]:
                cheapest_path = (a_times, b_times, game_machine.tokens)
    return cheapest_path


# read game machine configurations, find the cheapest path to the prize
with open("day13/input.txt") as f:
    cost = 0
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
                [int(x) for x in _line.strip("Prize: X=").replace("Y=", "").split(", ")]
            )
            gm = GameMachine(buttons["A"], buttons["B"], prize)
            cheapest_path = find_cheapest_path(gm)
            if cheapest_path[2] is not None:
                cost += cheapest_path[2]

print("Part 1:", cost)
