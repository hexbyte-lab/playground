# this code is from the internet and it is not my own
# problem: https://leetcode.com/problems/count-the-number-of-computer-unlocking-permutations/
 
import time
from typing import List

def countPermutations(complexity: List[int]) -> int:
    n = len(complexity)
    
    for i in range(n):
        if complexity[i] <= complexity[0]:
            return 0
        
    count, mod = 1, 10**9 + 7
    for i in range(2, n):
        count = (count * i) % mod
    return count

# Solution:
# The password complexity of the computer with index 0 is denoted as T=complexity[0].

# If there exists a computer with an index greater than 0
# whose password complexity is less than or equal to T,
# then we should pick the one with the smallest password complexity.

# Since no computer has a smaller complexity than that,
# it can never be unlocked, so the answer is 0.

# If no such computer exists,
# then every computer can be unlocked by computer 0 at the start,
# and the rest can be unlocked in any order.
# Thus, the answer is (n−1)!.


# Time Complexity: O(n)
# Space Complexity: O(1)

# start time
start_time = time.time()
print(countPermutations(complexity = [260,95,106,175,392,241,476,19,293,127,44,287,415,498,194,196,375,78,108]))
end_time = time.time()
print(f"Time taken: {end_time - start_time} seconds")