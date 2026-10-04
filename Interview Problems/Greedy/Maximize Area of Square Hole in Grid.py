"""
Maximize Area of Square Hole in Grid
Source: https://leetcode.com/problems/maximize-area-of-square-hole-in-grid/

A grid has n + 2 horizontal and m + 2 vertical bars (indexed from 1). Only the
bars listed in hBars / vBars may be removed. Removing a set of consecutive
removable bars merges cells into a larger hole. Return the maximum area of a
square hole obtainable.

Example:
    Input:  n = 2, m = 1, hBars = [2, 3], vBars = [2]
    Output: 4

Approach:
    Removing a run of L consecutive removable bars opens a gap spanning L + 1
    cells in that direction. So find the longest run of consecutive integers in
    hBars and in vBars; the square's side is min(runH, runV) + 1 and the area is
    that side squared.

    Note: it is NOT the largest gap between sorted bars -- a big gap can be made
    of fixed (non-removable) bars and cannot be opened.

Complexity: Time O(h log h + v log v) | Space O(1)
"""

from typing import List


class Solution:
    def maximizeSquareHoleArea(
        self, n: int, m: int, hBars: List[int], vBars: List[int]
    ) -> int:
        def longest_consecutive_run(bars: List[int]) -> int:
            bars.sort()
            best = run = 1
            for i in range(1, len(bars)):
                if bars[i] == bars[i - 1] + 1:
                    run += 1
                    best = max(best, run)
                else:
                    run = 1
            return best

        side = min(longest_consecutive_run(hBars), longest_consecutive_run(vBars)) + 1
        return side * side


if __name__ == "__main__":
    s = Solution()
    print(s.maximizeSquareHoleArea(2, 1, [2, 3], [2]))           # 4
    print(s.maximizeSquareHoleArea(1, 1, [2], [2]))             # 4
    print(s.maximizeSquareHoleArea(2, 3, [2, 3], [2, 3, 4]))    # 9
