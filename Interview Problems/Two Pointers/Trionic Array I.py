"""
Trionic Array I

An array is "trionic" if it can be split into three strictly monotonic parts:
first strictly increasing, then strictly decreasing, then strictly increasing
again, where each of the three parts is non-empty. Return whether nums is trionic.

Example:
    Input:  nums = [1, 3, 5, 4, 2, 6]
    Output: True        # up [1,3,5] -> down [5,4,2] -> up [2,6]

Approach:
    Walk one index through the array in three phases (up, down, up), advancing
    only while the required strict relation holds. The array is trionic iff every
    phase made real progress and the walk ends exactly at the last element.

Complexity: Time O(n) | Space O(1)
"""

from typing import List


class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        n = len(nums)
        i = 0

        # Phase 1: strictly increasing
        while i + 1 < n and nums[i] < nums[i + 1]:
            i += 1
        if i == 0 or i == n - 1:
            return False  # the first peak cannot be the start or the end

        # Phase 2: strictly decreasing
        peak = i
        while i + 1 < n and nums[i] > nums[i + 1]:
            i += 1
        if i == peak or i == n - 1:
            return False  # must have a decreasing part with room to rise again

        # Phase 3: strictly increasing again
        while i + 1 < n and nums[i] < nums[i + 1]:
            i += 1

        return i == n - 1


if __name__ == "__main__":
    s = Solution()
    print(s.isTrionic([1, 3, 5, 4, 2, 6]))  # True
    print(s.isTrionic([1, 2, 3, 4]))        # False
