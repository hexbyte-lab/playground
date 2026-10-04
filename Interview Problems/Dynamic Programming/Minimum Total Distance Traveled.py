"""
Minimum Total Distance Traveled
Source: https://leetcode.com/problems/minimum-total-distance-traveled/

Robots sit at positions on a number line; factories each sit at a position and
can repair up to a given limit of robots. Every robot must reach some factory.
Return the minimum total distance all robots travel.

Example:
    Input:  robot = [0, 4, 6], factory = [[2, 2], [6, 2]]
    Output: 4

Approach:
    Sort both robots and factories. In sorted order an optimal assignment never
    "crosses", so define solve(i, j) = min distance to repair robots[i:] using
    factories[j:]. For factory j we either skip it, or send its first 1..limit
    robots to it and recurse. Memoize on (i, j).

Complexity: Time O(n * m * limit) | Space O(n * m)
"""

from functools import cache
from typing import List


class Solution:
    def minimumTotalDistance(
        self, robot: List[int], factory: List[List[int]]
    ) -> int:
        robot.sort()
        factory.sort()
        n = len(robot)
        m = len(factory)
        INF = float("inf")

        @cache
        def solve(i: int, j: int) -> float:
            if i == n:
                return 0          # all robots assigned
            if j == m:
                return INF        # robots left but no factories
            pos, limit = factory[j]
            best = solve(i, j + 1)  # skip this factory
            cost = 0
            for k in range(1, limit + 1):
                if i + k - 1 >= n:
                    break
                cost += abs(robot[i + k - 1] - pos)
                sub = solve(i + k, j + 1)
                if sub != INF:
                    best = min(best, cost + sub)
            return best

        return int(solve(0, 0))


if __name__ == "__main__":
    s = Solution()
    print(s.minimumTotalDistance([0, 4, 6], [[2, 2], [6, 2]]))   # 4
    print(s.minimumTotalDistance([1, -1], [[-2, 1], [2, 1]]))    # 2
