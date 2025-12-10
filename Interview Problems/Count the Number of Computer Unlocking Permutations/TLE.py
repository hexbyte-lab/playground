# TLE and MLE for this case:
# complexity = [3470,9997,31628,55082,43915,14129,
# 49183,99427,71495,31577,74287,96625,
# 55548,56522,45502,20407,24812,48500,
# 48200,57692,20660,50351,29619,88947,
# 65929,3471,37527,17931,62499,69198,
# 45737,38605,94241,68261,61653,97116,
# 97217,79694,58943,54248,24192,39712,
# 34398,84847,89541,90309,17607,67739,84663,35600]

import time
from typing import List

def countPermutations(complexity: List[int]) -> int:
    n = len(complexity)
    MOD = 10**9 + 7

    # dependency graph
    graph: dict[int, List[int]] = {i: [] for i in range(n)}
    for i in range(1, n):
        for j in range(i):
            if complexity[j] < complexity[i]:
                graph[i].append(j)

    # dp array
    dp: List[int] = [0] * (1 << n)  # (1 << n) is 2^n
    dp[1 << 0] = 1  # 0th computer is unlocked

    # iterate over all masks,
    for mask in range(1 << n):
        for i in range(n):
            # if i is not yet unlocked in this mask
            if (mask & (1 << i)) == 0:  # basically means i is not in the mask
                canUnlock = any(
                    (mask & (1 << parent)) != 0 for parent in graph[i]
                )  # basically means if any parent is in the mask
                if canUnlock:
                    newMask = mask | (1 << i)  # basically means i is now in the mask
                    dp[newMask] = (dp[newMask] + dp[mask]) % MOD

    # return the number of permutations for the last mask
    return dp[(1 << n) - 1]

# start time
start_time = time.time()
print(countPermutations(complexity = [260,95,106,175,392,241,476,19,293,127,44,287,415,498,194,196,375,78,108])) # Output: 2
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")