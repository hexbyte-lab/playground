from functools import cache


class Solution:
    def minimumTotalDistance(self, robot, factory):
        robot.sort()
        factory.sort()
        n = len(robot)
        m = len(factory)
        INF = float('inf')

        @cache
        def solve(i, j):
            if i == n:
                return 0
            if j == m:
                return INF
            pos, lim = factory[j]
            best = solve(i, j + 1)  # skip this factory
            cost = 0
            for k in range(1, lim + 1):
                if i + k - 1 >= n:
                    break
                cost += abs(robot[i + k - 1] - pos)
                sub = solve(i + k, j + 1)
                if sub != INF:
                    best = min(best, cost + sub)
            return best

        return solve(0, 0)
