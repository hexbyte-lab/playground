"""
Four Divisors
Source: https://leetcode.com/problems/four-divisors/

Return the sum of divisors of every integer in nums that has exactly four
divisors. If no such integer exists, return 0.

Example:
    Input:  nums = [21, 4, 7]
    Output: 32          # 21 has divisors 1, 3, 7, 21 (sum 32); the others do not

Approach:
    For each number collect divisors up to its square root (adding the paired
    divisor n // i). Keep only numbers with exactly four divisors and add their
    divisor sums. A memo avoids recomputing repeated values.

Complexity: Time O(k * sqrt(max)) | Space O(k)   # k = len(nums)
"""

from typing import List


class Solution:
    def sumFourDivisors(self, nums: List[int]) -> int:
        memo: dict[int, List[int]] = {}

        def divisors(n: int) -> List[int]:
            if n in memo:
                return memo[n]
            found = []
            for i in range(1, int(n**0.5) + 1):
                if n % i == 0:
                    found.append(i)
                    if i != n // i:
                        found.append(n // i)
            memo[n] = found
            return found

        total = 0
        for num in nums:
            divs = divisors(num)
            if len(divs) == 4:
                total += sum(divs)
        return total


if __name__ == "__main__":
    s = Solution()
    print(s.sumFourDivisors([21, 4, 7]))  # 32
    print(s.sumFourDivisors([21, 21]))    # 64
