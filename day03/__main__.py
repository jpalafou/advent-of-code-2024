def mul_parser(s: str):
    start_idx = s.find("mul(")
    if start_idx == -1:
        return 0
    start_idx += 4
    stop_idx = s.find(")", start_idx)
    if stop_idx == -1:
        return 0
    arguments = s[start_idx:stop_idx].split(",")
    try:
        if len(arguments) != 2:
            raise ValueError
        product = int(arguments[0]) * int(arguments[1])
        new_start_idx = stop_idx + 1
        return product + mul_parser(s[new_start_idx:])
    except ValueError:
        return mul_parser(s[start_idx:])


def do_dont_mul_parser(s: str, do=True):
    left_of_switch_idx = s.find("don't()") if do else s.find("do()")
    if left_of_switch_idx == -1:
        return mul_parser(s) if do else 0
    right_of_switch_idx = left_of_switch_idx + (7 if do else 4)
    return (mul_parser(s[:left_of_switch_idx]) if do else 0) + do_dont_mul_parser(
        s[right_of_switch_idx:], not do
    )

    left_of_dont_idx = s.find("don't()")
    if left_of_dont_idx == -1:
        return mul_parser(s)
    right_of_dont_idx = left_of_dont_idx + 7
    return mul_parser(s[:left_of_dont_idx]) + do_dont_mul_parser(s[right_of_dont_idx:])


# read data as a single line of text
with open("day03/input.txt") as f:
    concatenated_line = ""
    for line in f:
        concatenated_line += line.strip()

# parse the concatenated line
valid_product_sum = mul_parser(concatenated_line.strip())
valid_product_sum_do_dont = do_dont_mul_parser(concatenated_line.strip())

# print the results
print("Part 1:", valid_product_sum)
print("Part 2:", valid_product_sum_do_dont)
