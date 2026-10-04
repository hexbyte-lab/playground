"""
Find All Numbers Disappeared in an Array
Source: https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/

Given an array nums of n integers where each value is in the range [1, n],
return every value in [1, n] that does not appear in nums.

Example:
    Input:  nums = [4, 3, 2, 7, 8, 2, 3, 1]
    Output: [5, 6]

Approach:
    Use the array itself as a hash set. For each value v, flip the sign of the
    element at index v - 1 to mark "v is present". Afterwards, any index that is
    still positive corresponds to a missing value (index + 1).

Complexity: Time O(n) | Space O(1)   # in place, ignoring the output list
"""

from typing import List


class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:
        n = len(nums)
        for i in range(n):
            index = abs(nums[i]) - 1
            if nums[index] > 0:
                nums[index] = -nums[index]

        return [i + 1 for i in range(n) if nums[i] > 0]


if __name__ == "__main__":
    s = Solution()
    print(s.findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # [5, 6]
    print(s.findDisappearedNumbers([1, 1]))                    # [2]
