"""
Construct the Minimum Bitwise Array I
Source: https://leetcode.com/problems/construct-the-minimum-bitwise-array-i/

You are given an array nums of prime numbers. For each nums[i], find the
smallest non-negative ans[i] such that ans[i] OR (ans[i] + 1) == nums[i].
If no such value exists, use -1.

Example:
    Input:  nums = [2, 3, 5, 7]
    Output: [-1, 1, 4, 3]

Approach:
    For each number, scan candidates upward and return the first one whose
    OR with its successor reproduces the target. (Constraints for the "I"
    variant are small, so the linear scan is fine.)

Complexity: Time O(sum(nums)) | Space O(1)   # excluding the output list
"""

from typing import List


class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        result = []
        for num in nums:
            answer = -1
            for candidate in range(1, num):
                if candidate | (candidate + 1) == num:
                    answer = candidate
                    break
            result.append(answer)
        return result


if __name__ == "__main__":
    s = Solution()
    print(s.minBitwiseArray([2, 3, 5, 7]))  # [-1, 1, 4, 3]
