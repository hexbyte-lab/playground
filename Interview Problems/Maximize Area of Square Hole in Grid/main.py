"""
Problem Description:
You are given the two integers, n and m and two integer arrays, hBars and vBars.
The grid has n + 2 horizontal and m + 2 vertical bars, creating 1 x 1 unit cells.
The bars are indexed starting from 1.

You can remove some of the bars in hBars from horizontal bars
and some of the bars in vBars from vertical bars.
Note that other bars are fixed and cannot be removed.

Return an integer denoting the maximum area of a square-shaped hole in the grid,
after removing some bars (possibly none).


So the problem bassicaly says that
we have a grid of size n x m with horizontal and vertical bars.
We need to find the maximum area of a square hole that can be formed
from the grid by removing some bars.

Example:

Input: n = 2, m = 1, hBars = [2,3], vBars = [2]
Output: 4

Explanation:

The left image shows the initial grid formed by the bars.
The horizontal bars are [1,2,3,4], and the vertical bars are [1,2,3].

One way to get the maximum square-shaped hole
is by removing horizontal bar 2 and vertical bar 2.

Solution:
To solve this problem, we can follow these steps:
1. Add the boundaries (0 and n+1 for horizontal bars, 0 and m+1 for vertical bars)
   to the respective lists of bars.
2. Sort the hBars and vBars arrays.
3. Find the maximum gap between consecutive bars in hBars and vBars.
4. The result will be the square of the minimum of these two maximum gaps.
5. Return the result.

so for the given example Input: n = 2, m = 1, hBars = [2,3], vBars = [2]:
The horizontal bars after adding boundaries will be [0,1,2,3,4]
and the vertical bars will be [0,1,2,3].
The maximum gap in horizontal bars is 2 (between 1 and 3),
and the maximum gap in vertical bars is 2 (between 1 and 3).


"""


from typing import List


class Solution:
    def maximizeSquareHoleArea(self, n: int, m: int, hBars: List[int], vBars: List[int]) -> int:
        # Add boundaries to the bars
        hBars = [0] + sorted(hBars) + [n + 1]
        vBars = [0] + sorted(vBars) + [m + 1]

        # Find maximum gaps
        max_h_gap = 0
        max_v_gap = 0
        for i in range(1, len(hBars)):
            if hBars[i] - hBars[i - 1] > max_h_gap:
                max_h_gap = hBars[i] - hBars[i - 1]
        
        for i in range(1, len(vBars)):
            if vBars[i] - vBars[i - 1] > max_v_gap:
                max_v_gap = vBars[i] - vBars[i - 1]
        
        # Calculate the area of the largest square hole
        max_square_side = min(max_h_gap, max_v_gap)
        return max_square_side * max_square_side

# Example usage
solution = Solution()
result = solution.maximizeSquareHoleArea(2, 1, [2, 3], [2])
print(result)  # Output: 4