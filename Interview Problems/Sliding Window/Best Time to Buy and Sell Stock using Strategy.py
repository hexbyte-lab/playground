"""
Best Time to Buy and Sell Stock using Strategy
Source: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/

You are given prices and a strategy array of the same length (each entry -1, 0,
or 1) plus an even integer k. Profit is sum(strategy[i] * prices[i]). You may
perform at most one modification: pick a window of exactly k consecutive indices,
set the first k/2 of them to 0 and the last k/2 to 1. Return the maximum profit.

Example:
    Input:  prices = [4, 2, 8], strategy = [-1, 0, 1], k = 2
    Output: 10

Approach:
    The original profit is fixed. For a window starting at i, the profit change
    ("delta") is: the first half loses its contribution (becomes 0) and the
    second half becomes (1 - strategy) * price. Precompute prefix sums of both
    "set to 0" and "set to 1" deltas so each window's delta is O(1); the answer
    is original profit plus the best non-negative delta (0 = no modification).

Complexity: Time O(n) | Space O(n)
"""

from typing import List


class Solution:
    def maxProfit(self, prices: List[int], strategy: List[int], k: int) -> int:
        n = len(prices)
        half = k // 2

        original = sum(strategy[i] * prices[i] for i in range(n))

        # delta_zero[i]: change if index i is forced to 0  (loses strategy*price)
        # delta_one[i] : change if index i is forced to 1  (gains (1-strategy)*price)
        prefix_zero = [0] * (n + 1)
        prefix_one = [0] * (n + 1)
        for i in range(n):
            prefix_zero[i + 1] = prefix_zero[i] - strategy[i] * prices[i]
            prefix_one[i + 1] = prefix_one[i] + (1 - strategy[i]) * prices[i]

        best_delta = 0  # no modification
        for i in range(n - k + 1):
            first_half = prefix_zero[i + half] - prefix_zero[i]
            second_half = prefix_one[i + k] - prefix_one[i + half]
            best_delta = max(best_delta, first_half + second_half)

        return original + best_delta


if __name__ == "__main__":
    s = Solution()
    print(s.maxProfit([4, 2, 8], [-1, 0, 1], 2))  # 10
    print(s.maxProfit([5, 4, 3], [1, 1, 0], 2))   # 9
