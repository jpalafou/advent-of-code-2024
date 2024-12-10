from itertools import product


def _operate(x1, x2, op):
    if op == "+":
        return x1 + x2
    elif op == "*":
        return x1 * x2


def operate(x, ops):
    out = _operate(x[0], x[1], ops[0])
    for i in range(1, len(ops)):
        out = _operate(out, x[i + 1], ops[i])
    return out


# read input, count lines which can be made true
sum_possibly_true = 0
with open("day07/input.txt") as f:
    for line in f:
        test_str, args_str = line.strip().split(": ")
        test, args = int(test_str), list(map(int, args_str.split()))

        for ops in product(["+", "*"], repeat=len(args) - 1):
            if operate(args, ops) == test:
                sum_possibly_true += test
                break
print("Part 1:", sum_possibly_true)
