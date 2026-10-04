"""
Minimum Distance to the Target Element
Source: https://leetcode.com/problems/minimum-distance-to-the-target-element/

Given nums, a target value, and a start index, return the minimum value of
abs(i - start) over every index i where nums[i] == target.

Example:
    Input:  nums = [1, 2, 3, 4, 5], target = 5, start = 3
    Output: 1            # target 5 is at index 4, |4 - 3| = 1

Approach:
    Scan the array and, for every position holding the target, track the
    smallest distance to start.

Complexity: Time O(n) | Space O(1)
"""

from typing import List


class Solution:
    def getMinDistance(self, nums: List[int], target: int, start: int) -> int:
        return min(abs(i - start) for i, num in enumerate(nums) if num == target)


if __name__ == "__main__":
    s = Solution()
    print(s.getMinDistance([1, 2, 3, 4, 5], 5, 3))  # 1
    print(s.getMinDistance([1], 1, 0))              # 0
