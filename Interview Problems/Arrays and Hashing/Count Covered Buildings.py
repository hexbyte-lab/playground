"""
Count Covered Buildings
Source: https://leetcode.com/problems/count-covered-buildings/

Given a grid of size n x n and a list of building coordinates [x, y], a building
is "covered" if there is at least one other building above it, below it, to its
left, and to its right (sharing its row or column). Return the covered count.

Example:
    Input:  n = 5, buildings = [[1,3],[3,2],[3,3],[3,5],[5,3]]
    Output: 1            # only (3, 3) is covered on all four sides

Approach:
    Precompute, for each row, the min and max occupied y, and for each column,
    the min and max occupied x. A building (x, y) is covered iff it lies strictly
    inside both its row's y-bounds and its column's x-bounds.

Complexity: Time O(n) | Space O(n)   # n = number of buildings
"""

from typing import List
from collections import defaultdict


class Solution:
    def countCoveredBuildings(self, n: int, buildings: List[List[int]]) -> int:
        min_y_for_row = defaultdict(lambda: float("inf"))
        max_y_for_row = defaultdict(lambda: float("-inf"))
        min_x_for_col = defaultdict(lambda: float("inf"))
        max_x_for_col = defaultdict(lambda: float("-inf"))

        for x, y in buildings:
            min_y_for_row[x] = min(min_y_for_row[x], y)
            max_y_for_row[x] = max(max_y_for_row[x], y)
            min_x_for_col[y] = min(min_x_for_col[y], x)
            max_x_for_col[y] = max(max_x_for_col[y], x)

        covered = 0
        for x, y in buildings:
            if (min_y_for_row[x] < y < max_y_for_row[x]
                    and min_x_for_col[y] < x < max_x_for_col[y]):
                covered += 1
        return covered


if __name__ == "__main__":
    s = Solution()
    print(s.countCoveredBuildings(5, [[1, 2], [2, 3], [3, 4], [4, 5]]))          # 0
    print(s.countCoveredBuildings(5, [[1, 3], [3, 2], [3, 3], [3, 5], [5, 3]]))  # 1
