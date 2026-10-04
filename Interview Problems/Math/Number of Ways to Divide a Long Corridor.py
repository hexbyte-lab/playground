"""
Number of Ways to Divide a Long Corridor
Source: https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/

A corridor is a string of 'S' (seat) and 'P' (plant). A valid division places
dividers so every section contains exactly two seats. Return the number of valid
divisions modulo 1e9 + 7.

Example:
    Input:  corridor = "SSPPSPS"
    Output: 3

Approach:
    There must be a positive, even number of seats. Group seats into consecutive
    pairs (seats 1-2, 3-4, ...). Between one pair's second seat and the next
    pair's first seat there are g gap cells, giving g + 1 places to drop the
    divider. Multiply these choices across all gaps.

Complexity: Time O(n) | Space O(s)   # s = number of seats
"""

MOD = 10**9 + 7


class Solution:
    def numberOfWays(self, corridor: str) -> int:
        seat_positions = [i for i, cell in enumerate(corridor) if cell == "S"]
        seats = len(seat_positions)

        if seats == 0 or seats % 2 != 0:
            return 0

        ways = 1
        # gap between the end of one seat-pair and the start of the next
        for pair in range(2, seats, 2):
            gap = seat_positions[pair] - seat_positions[pair - 1]
            ways = (ways * gap) % MOD
        return ways


if __name__ == "__main__":
    s = Solution()
    print(s.numberOfWays("SSPPSPS"))  # 3
    print(s.numberOfWays("PPSPSP"))   # 1
