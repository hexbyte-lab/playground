"""
Valid Anagram
Source: https://leetcode.com/problems/valid-anagram/

Given two strings s and t, return True if t is an anagram of s
(uses exactly the same characters with the same counts), else False.

Example:
    Input:  s = "anagram", t = "nagaram"
    Output: True

Approach:
    Count how often each character appears in both strings and compare the
    two count maps. Equal maps means equal multisets of characters.

Complexity: Time O(n) | Space O(1)   # at most 26 lowercase letters
"""


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        s_counts: dict[str, int] = {}
        t_counts: dict[str, int] = {}

        for char in s:
            s_counts[char] = s_counts.get(char, 0) + 1
        for char in t:
            t_counts[char] = t_counts.get(char, 0) + 1

        return s_counts == t_counts


if __name__ == "__main__":
    s = Solution()
    print(s.isAnagram("anagram", "nagaram"))  # True
    print(s.isAnagram("rat", "car"))          # False
