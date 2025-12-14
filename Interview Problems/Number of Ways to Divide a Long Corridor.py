"""
problem: https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/
"""

def numberOfWays(corridor: str) -> int:
    seat_count = corridor.count("S")
    
    if seat_count % 2 != 0 or seat_count == 0:
        return 0
    
    # group seats into pairs
    pairs = []
    current_pair = []
    
    for i in range(len(corridor)):
        if corridor[i] == "S":
            current_pair.append(i)
            if len(current_pair) == 2:
                pairs.append(current_pair)
                current_pair = []
    
    # if we have k plants between two pairs, we can place a divider in k+1 ways
    ways = 1
    for i in range(len(pairs) - 1):
        ways *= (pairs[i+1][0] - pairs[i][1])

    
    return ways % (10**9 + 7)

"""
Solution:
1. Count the number of seats
2. If the number of seats is odd or zero, return 0
3. Group the seats into pairs
4. If we have k plants between two pairs, we can place a divider in k+1 ways
5. Return the number of ways modulo 10^9 + 7
"""

print(numberOfWays("SSPPSPS")) # output: 3
print(numberOfWays("PPSPSP")) # output: 1