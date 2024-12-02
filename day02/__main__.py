import numpy as np


# helper function
def is_safe(report: np.ndarray) -> bool:
    report_diffs = np.diff(report)
    all_increasing_or_decreasing = np.all(report_diffs < 0) or np.all(report_diffs > 0)
    all_magnitudes_within_bounds = np.all(np.abs(report_diffs) >= 1) and np.all(
        np.abs(report_diffs) <= 3
    )
    return all_increasing_or_decreasing and all_magnitudes_within_bounds


# read the data
with open("day02/input.txt") as f:
    n_valid = 0
    n_valid_with_removal = 0
    for line in f:
        # import line as numpy array
        report = np.array([int(x) for x in line.strip().split(" ")])

        # check if report is valid for different safety rules
        n_valid += is_safe(report)
        n_valid_with_removal += any(
            is_safe(np.delete(report, i)) for i in range(len(report))
        )

# print both totals
print("Part 1:", n_valid)
print("Part 2:", n_valid_with_removal)
