"""
Problem: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-using-strategy/description/
"""

from typing import List


def maxProfit(prices: List[int], strategy: List[int], k: int) -> int:
    n = len(prices)
    half = k // 2

    # Original profit
    orig_prof = sum(strategy[i] * prices[i] for i in range(n))


    A = [-strategy[i] * prices[i] for i in range(n)] # holding the stock
    B = [(1 - strategy[i]) * prices[i] for i in range(n)] # selling the stock

    # build prefix sums
    prefixA = [0] * (n + 1)
    prefixB = [0] * (n + 1)
    for i in range(n):
        prefixA[i + 1] = prefixA[i] + A[i]
        prefixB[i + 1] = prefixB[i] + B[i]
        

    # Find the maximum delta from any valid modification (With the help of chatGPT)
    max_delta = 0  # No modification = 0 delta
    for i in range(n - k + 1):
        # First half [i, i + half): set to 0
        first_half_delta = prefixA[i + half] - prefixA[i]
        # Second half [i + half, i + k): set to 1
        second_half_delta = prefixB[i + k] - prefixB[i + half]
        total_delta = first_half_delta + second_half_delta
        max_delta = max(max_delta, total_delta)

    return orig_prof + max_delta


"""
Solution:
- Compute original profit as sum(strategy[i] * prices[i])
- For each position, compute the delta if we modify k consecutive elements:
  - First k/2 elements become 0: delta = -strategy[i] * prices[i]
  - Last k/2 elements become 1: delta = (1 - strategy[i]) * prices[i]
- Use prefix sums to efficiently compute the delta for each starting position
- Return original_profit + max(0, best_delta)

Time complexity: O(n)
Space complexity: O(n)
"""

print(maxProfit([4, 2, 8], [-1, 0, 1], 2))  # Output: 10
print(maxProfit([5, 4, 3], [1, 1, 0], 2))  # Output: 9

