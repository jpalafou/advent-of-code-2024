import numpy as np

# read the data
with open("day02/input.txt") as f:
    n_valid = 0
    for line in f:
        # import line as numpy array, compute adjacent differences
        report = np.array([int(x) for x in line.strip().split(" ")])
        report_diffs = np.diff(report)

        # check if all differences are either all increasing or decreasing by 1-3
        all_increasing_or_decreasing = np.all(report_diffs < 0) or np.all(
            report_diffs > 0
        )
        all_magnitudes_within_bounds = np.all(np.abs(report_diffs) >= 1) and np.all(
            np.abs(report_diffs) <= 3
        )

        # increment valid report count
        n_valid += int(all_increasing_or_decreasing and all_magnitudes_within_bounds)

# print valid report count
print("Part 1:", n_valid)
