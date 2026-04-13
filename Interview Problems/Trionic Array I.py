from typing import List
class Solution:
    def isTrionic(self, nums: List[int]) -> bool:
        # check if nums[0...p] is strictly increasing
        n = len(nums)
        i = 0
        while i + 1 < n and nums[i] < nums[i + 1]:
            i += 1
        if i == 0 or i == n - 1:
            return False  # peak cannot be first or last element
        # check if nums[p...q] is strictly decreasing
        p = i
        while i + 1 < n and nums[i] > nums[i + 1]:
            i += 1
        if i == p or i == n -1:
            return False  # must have decreasing part
        
        # check if nums[q...end] is strictly increasing
        while i + 1 < n and nums[i] < nums[i + 1]:
            i += 1
        
        return i == n - 1
    
print(Solution().isTrionic([1,3,5,4,2,6]))  # True