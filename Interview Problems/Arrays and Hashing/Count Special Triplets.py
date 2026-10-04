"""
Count Special Triplets

Given an array nums, count index triplets (i, j, k) with i < j < k where the
middle element is doubled on both sides, i.e. nums[i] == 2 * nums[j] and
nums[k] == 2 * nums[j]. Return the count modulo 1e9 + 7.

Example:
    Input:  nums = [8, 4, 2, 8, 4]
    Output: 2

Approach:
    Treat each index as the middle element j. For value v = nums[j] we need the
    value 2 * v on its left and on its right. Keep a running "left" count map as
    we scan; the right count is (total occurrences) - (left occurrences). The
    triplets centered at j is left_count * right_count.

Complexity: Time O(n) | Space O(n)
"""

from typing import List

MOD = 10**9 + 7


class Solution:
    def specialTriplets(self, nums: List[int]) -> int:
        total_count: dict[int, int] = {}
        for num in nums:
            total_count[num] = total_count.get(num, 0) + 1

        left_count: dict[int, int] = {}
        triplets = 0
        for num in nums:
            target = num * 2
            left = left_count.get(target, 0)
            left_count[num] = left_count.get(num, 0) + 1
            right = total_count.get(target, 0) - left_count.get(target, 0)
            triplets += left * right

        return triplets % MOD


if __name__ == "__main__":
    s = Solution()
    print(s.specialTriplets([8, 4, 2, 8, 4]))  # 2
