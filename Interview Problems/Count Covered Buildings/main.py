# problem: https://leetcode.com/problems/count-covered-buildings/

import time
from typing import List
from collections import defaultdict


def countCoveredBuildings(n: int, buildings: List[List[int]]) -> int:
    # Preprocess min/max for rows and columns
    min_y_for_row = defaultdict(lambda: float("inf"))
    max_y_for_row = defaultdict(lambda: float("-inf"))
    min_x_for_col = defaultdict(lambda: float("inf"))
    max_x_for_col = defaultdict(lambda: float("-inf"))

    for x, y in buildings:
        min_y_for_row[x] = min(min_y_for_row[x], y)
        max_y_for_row[x] = max(max_y_for_row[x], y)
        min_x_for_col[y] = min(min_x_for_col[y], x)
        max_x_for_col[y] = max(max_x_for_col[y], x)

    # Count covered buildings
    covered = 0
    for x, y in buildings:
        if (
            min_y_for_row[x] < y < max_y_for_row[x]
            and min_x_for_col[y] < x < max_x_for_col[y]
        ):
            covered += 1

    return covered


# Solution:
# A building at (x, y) is "covered" if there exists:
# - A building above it (same column, larger x)
# - A building below it (same column, smaller x)
# - A building to its left (same row, smaller y)
# - A building to its right (same row, larger y)
#
# We precompute min/max x for each column and min/max y for each row.
# Then check if each building is strictly between these bounds.

# Time Complexity: O(n) where n is number of buildings
# Space Complexity: O(n) for the hashmaps


start_time = time.time()
print(countCoveredBuildings(5, [[1, 2], [2, 3], [3, 4], [4, 5]]))  # Expected: 0
print(
    countCoveredBuildings(5, [[1, 3], [3, 2], [3, 3], [3, 5], [5, 3]])
)  # Expected: 1 (only (3,3) is covered)
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")
