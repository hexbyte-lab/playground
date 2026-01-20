from typing import List 
        
class Solution:
    def minBitwiseArray(self, nums: List[int]) -> List[int]:
        result = []
        
        for num in nums:
            copy = num
            current = -1
            for i in range(1, copy):
                if(i | (i + 1)) == copy:
                    current = i
                    break
            result.append(current)
            
        return result
            