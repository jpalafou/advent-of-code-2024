"""
Advent of Code 2024 - Day 11 Solution
--------------------------------------
Author: Jonathan Palafoutas
Date: December 11, 2024

Acknowledgements:
    - Jack Draney for suggesting the use of a counter to improve performance.
"""

from functools import lru_cache


@lru_cache(maxsize=None)
def process(stone):
    if stone == 0:
        return (1,)
    stone_str = str(stone)
    if len(stone_str) % 2 == 0:
        half_len = len(stone_str) // 2
        return int(stone_str[:half_len]), int(stone_str[half_len:])
    return (stone * 2024,)


def update_counter(counter, key, count=1):
    if key in counter:
        counter[key] += count
    else:
        counter[key] = count


def blink(stone_counter, n):
    for _ in range(n):
        new_stone_counter = {}
        for stone in stone_counter:
            for new_stone in process(stone):
                update_counter(new_stone_counter, new_stone, stone_counter[stone])
        stone_counter = new_stone_counter
    return stone_counter


# read initial stones
stone_counter = {}
with open("day11/input.txt") as f:
    for stone in f.read().split(" "):
        update_counter(stone_counter, int(stone))

# blink 25 times and print the number of stone_counter
stone_counter = blink(stone_counter, 25)
print("Part 1:", sum(stone_counter.values()))

# blink 50 more times and print the result
stone_counter = blink(stone_counter, 50)
print("Part 2:", sum(stone_counter.values()))
