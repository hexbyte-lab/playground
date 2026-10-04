"""
Number of Smooth Descent Periods of a Stock
Source: https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/

A "smooth descent period" is a contiguous subarray where each day's price is
exactly 1 less than the previous day's (a single day counts). Return how many
such subarrays exist.

Example:
    Input:  prices = [3, 2, 1, 4]
    Output: 7

Approach:
    Count periods that END at each index i. If prices[i] == prices[i-1] - 1 the
    current descent streak grows by one, otherwise it resets to 1. The number of
    valid periods ending at i equals the current streak length, so summing the
    streak across all indices gives the answer.

Complexity: Time O(n) | Space O(1)
"""

from typing import List


class Solution:
    def getDescentPeriods(self, prices: List[int]) -> int:
        total = 0
        streak = 0
        for i in range(len(prices)):
            if i > 0 and prices[i] == prices[i - 1] - 1:
                streak += 1
            else:
                streak = 1
            total += streak
        return total


if __name__ == "__main__":
    s = Solution()
    print(s.getDescentPeriods([3, 2, 1, 4]))  # 7
    print(s.getDescentPeriods([8, 6, 7, 7]))  # 4
    print(s.getDescentPeriods([1]))           # 1
