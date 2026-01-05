from typing import List

"""

Given an integer array nums,
return the sum of divisors of the integers
in that array that have exactly four divisors.
Input: nums = [21,4,7]
Output: 32
Explanation: 
21 has 4 divisors: 1, 3, 7, 21
4 has 3 divisors: 1, 2, 4
7 has 2 divisors: 1, 7


in this example if save each calculation
we do to find how many divisors a number has,
we can avoid recalculating kind of like
divide and conquer, but with memoization.

here is a possible puseudo code:



"""

def sumFourDivisors(nums: List[int]) -> int:
    
    memo: dict= {}
    def getDivisors(n):
        if n in memo:
            return memo[n]
        divisors = []
        for i in range(1, int(n**0.5) + 1):
            if n % i == 0:
                divisors.append(i)
                if i != n // i:
                    divisors.append(n // i)
        memo[n] = divisors
        return divisors
    
    total = 0
    for num in nums:
        divisors = getDivisors(num)
        if len(divisors) == 4:
            total += sum(divisors)
    
    return total

# Example usage:
nums = [21, 4, 7]
print(sumFourDivisors(nums))  # Output: 32