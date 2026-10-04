"""
Longest Consecutive Sequence
Source: https://leetcode.com/problems/longest-consecutive-sequence/

Given an unsorted array of integers, return the length of the longest run of
consecutive integers. The algorithm must run in O(n) time.

Example:
    Input:  nums = [100, 4, 200, 1, 3, 2]
    Output: 4            # the run 1, 2, 3, 4

Approach:
    Put every value in a set for O(1) lookups. A value starts a new run only if
    value - 1 is absent, so we expand from each start and never re-walk a run.
    Each element is visited at most twice, giving O(n) overall.

Complexity: Time O(n) | Space O(n)
"""

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        num_set = set(nums)
        longest = 0

        for num in num_set:
            if num - 1 not in num_set:          # only start from a run's head
                current = num
                length = 1
                while current + 1 in num_set:
                    current += 1
                    length += 1
                longest = max(longest, length)

        return longest


if __name__ == "__main__":
    s = Solution()
    print(s.longestConsecutive([100, 4, 200, 1, 3, 2]))        # 4
    print(s.longestConsecutive([0, 3, 7, 2, 5, 8, 4, 6, 0, 1]))  # 9
