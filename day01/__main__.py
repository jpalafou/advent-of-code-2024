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

# compute frequency of each location
unique_locations1, frequency1 = np.unique(locations1, return_counts=True)
unique_locations2, frequency2 = np.unique(locations2, return_counts=True)

# create a matrix to store the frequency of each location
max_location = max(np.max(locations1), np.max(locations2))
location_count = np.zeros((max_location + 1, 2), dtype=int)
location_count[unique_locations1, 0] = frequency1
location_count[unique_locations2, 1] = frequency2

# array of all locations up to max_location
all_locations = np.arange(max_location + 1)

# compute the product of the frequency of each location weighted by the location
print("Part 2:", np.sum(np.prod(location_count, axis=1) * all_locations))
