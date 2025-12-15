"""
Problem: https://leetcode.com/problems/number-of-smooth-descent-periods-of-a-stock/description/
"""

from typing import List


def getDescentPeriods(prices: List[int]) -> int:
    n = len(prices)
    total = 0
    streak = 0

    for i in range(n):
        # If current price is exactly 1 less than previous, extend the streak
        if i > 0 and prices[i] == prices[i - 1] - 1:
            streak += 1
        else:
            streak = 1

        # Each position counts as a 'streak' number of smooth descent periods
        total += streak

    return total


"""
Solution: For each position i, count how many smooth descent periods end at that position
if prices[i] == prices[i-1] - 1, the streak continues (streak += 1)
otherwise, reset streak to 1 (single day is always a valid period)
the number of periods ending at position i equals the current streak length
Sum all streak values to get the total
"""

print(getDescentPeriods([3, 2, 1, 4]))  # Output: 7
print(getDescentPeriods([8, 6, 7, 7]))  # Output: 4
print(getDescentPeriods([1]))  # Output: 1
