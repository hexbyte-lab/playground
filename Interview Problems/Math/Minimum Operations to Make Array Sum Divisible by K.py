"""
Minimum Operations to Make Array Sum Divisible by K

Each operation picks an index i and replaces nums[i] with nums[i] - 1. Return
the minimum number of operations needed to make the sum of nums divisible by k.

Example:
    Input:  nums = [3, 9, 7], k = 5
    Output: 4            # sum is 19; 19 mod 5 = 4 decrements reach 15

Approach:
    Every operation lowers the total by exactly 1, so to reach the nearest lower
    multiple of k we need (sum mod k) operations (0 if already divisible).

Complexity: Time O(n) | Space O(1)
"""

from typing import List


class Solution:
    def minOperations(self, nums: List[int], k: int) -> int:
        return sum(nums) % k


if __name__ == "__main__":
    s = Solution()
    print(s.minOperations([3, 9, 7], 5))  # 4
    print(s.minOperations([5, 5], 5))     # 0
