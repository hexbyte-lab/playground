"""
Maximum Matrix Sum
Source: https://leetcode.com/problems/maximum-matrix-sum/

You may repeatedly pick two adjacent cells and multiply both by -1. Maximize the
sum of all matrix elements and return that maximum.

Example:
    Input:  matrix = [[1, 2, 3], [-1, -2, -3], [1, 2, 3]]
    Output: 16

Approach:
    A sign flip moves between two adjacent cells, so the parity of the negative
    count is all that matters. If the count of negatives is even, every value can
    be made positive -> sum of absolute values. If it is odd, one negative must
    remain, and it should be the smallest absolute value -> subtract twice that.

Complexity: Time O(n^2) | Space O(1)
"""

from typing import List


class Solution:
    def maxMatrixSum(self, matrix: List[List[int]]) -> int:
        negatives = 0
        min_abs = float("inf")
        total = 0

        for row in matrix:
            for val in row:
                total += abs(val)
                if val < 0:
                    negatives += 1
                min_abs = min(min_abs, abs(val))

        if negatives % 2 == 0:
            return total
        return total - 2 * int(min_abs)


if __name__ == "__main__":
    s = Solution()
    print(s.maxMatrixSum([[1, 2, 3], [-1, -2, -3], [1, 2, 3]]))  # 16
    print(s.maxMatrixSum([[-1, -1], [-1, -1]]))                  # 4
