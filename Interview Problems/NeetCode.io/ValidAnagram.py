class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        # Make them both dict
        s_dict: dict[str, int] = {}
        t_dict: dict[str, int] = {}
        
        # key value pair must be equal
        for char in s:
            s_dict[char] = s_dict.get(char, 0) + 1
        for char in t:
            t_dict[char] = t_dict.get(char, 0) + 1
            
        return s_dict == t_dict
    
solution = Solution()
print(solution.isAnagram("anagram", "nagaram"))