import numpy as np

# read the data
with open("day01/input.txt") as f:
    data = []
    for line in f:
        data.append([int(x) for x in line.strip().split("   ")])

# convert to numpy array
locations1, locations2 = np.array(data).T

# compute sum of distance of sorted locations
print("Part 1:", np.sum(np.abs(np.sort(locations1) - np.sort(locations2))))
