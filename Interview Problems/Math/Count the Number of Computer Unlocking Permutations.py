"""
Count the Number of Computer Unlocking Permutations
Source: https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/

Computer 0 is unlocked first; a locked computer i can be unlocked only by an
already-unlocked computer j with complexity[j] < complexity[i]. Return the number
of valid unlocking orders, modulo 1e9 + 7.

Example:
    Input:  complexity = [1, 2, 3]
    Output: 2            # computer 0 unlocks the rest in any of 2! orders

Approach:
    Computer 0 (complexity T = complexity[0]) is the only initial key. If any
    other computer has complexity <= T, nothing can ever unlock it, so the answer
    is 0. Otherwise computer 0 can unlock every other computer and the remaining
    n - 1 computers can be unlocked in any order: (n - 1)!.

Complexity: Time O(n) | Space O(1)
"""

from typing import List

MOD = 10**9 + 7


class Solution:
    def countPermutations(self, complexity: List[int]) -> int:
        n = len(complexity)

        # Start the scan at index 1: a later computer that is not harder than
        # computer 0 can never be unlocked.  (The original bug started at 0,
        # where complexity[0] <= complexity[0] always held and returned 0.)
        for i in range(1, n):
            if complexity[i] <= complexity[0]:
                return 0

        result = 1
        for i in range(2, n):  # (n - 1)!  ==  2 * 3 * ... * (n - 1)
            result = (result * i) % MOD
        return result


def count_permutations_bruteforce(complexity: List[int]) -> int:
    """Bitmask DP over unlocked subsets. Correct but O(2^n * n), so it TLEs for
    large inputs -- kept only to show the exponential baseline."""
    n = len(complexity)
    parents = {
        i: [j for j in range(i) if complexity[j] < complexity[i]] for i in range(n)
    }

    dp = [0] * (1 << n)
    dp[1 << 0] = 1  # computer 0 starts unlocked
    for mask in range(1 << n):
        for i in range(n):
            if mask & (1 << i):
                continue
            if any(mask & (1 << p) for p in parents[i]):
                dp[mask | (1 << i)] = (dp[mask | (1 << i)] + dp[mask]) % MOD
    return dp[(1 << n) - 1]


if __name__ == "__main__":
    s = Solution()
    print(s.countPermutations([1, 2, 3]))                  # 2
    print(s.countPermutations([3, 2, 1]))                  # 0  (2 and 1 <= 3)
    print(count_permutations_bruteforce([1, 2, 3]))        # 2  (matches, slowly)
