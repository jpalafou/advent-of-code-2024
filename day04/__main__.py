import numpy as np


def find_xmas(charr):
    return np.sum(
        np.all(
            np.array(
                [
                    charr[3, 3:],
                    np.diagonal(np.fliplr(charr))[3::-1],
                    charr[3::-1, 3],
                    np.diagonal(charr)[3::-1],
                    charr[3, 3::-1],
                    np.diagonal(np.fliplr(charr))[3::],
                    charr[3::, 3],
                    np.diagonal(charr)[3::],
                ]
            )
            == np.array([b"X", b"M", b"A", b"S"]),
            axis=1,
        )
    )


def find_x_mas(charr):
    target = [b"M", b"A", b"S"]
    diagonals = [np.diagonal(charr), np.diagonal(np.fliplr(charr))]
    return (
        sum(
            np.array_equal(diag, t)
            for diag in diagonals
            for t in (target, target[::-1])
        )
        == 2
    )


def search_padded(func, charr, pad_width):
    padded_charr = np.pad(
        charr, pad_width=pad_width, mode="constant", constant_values=b"*"
    )
    return sum(
        func(
            padded_charr[
                slice(i - pad_width, i + pad_width + 1),
                slice(j - pad_width, j + pad_width + 1),
            ]
        )
        for i in range(pad_width, padded_charr.shape[0] - pad_width)
        for j in range(pad_width, padded_charr.shape[1] - pad_width)
    )


# read the data as an array
with open("day04/input.txt") as file:
    rows = []
    for row in file:
        rows.append(list(row.strip()))
wordsearch = np.array(rows, dtype="S")


# count the number of XMAS occurrences in the wordsearch
n_xmas = search_padded(find_xmas, wordsearch, 3)
print("Part 1:", n_xmas)


# count the number of X-MAS occurrences in the wordsearch
n_x_mas = search_padded(find_x_mas, wordsearch, 1)
print("Part 2:", n_x_mas)
