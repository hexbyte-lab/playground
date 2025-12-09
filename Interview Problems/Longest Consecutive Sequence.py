# Problem: Given an unsorted array of integers nums,
# return the length of the longest consecutive elements sequence.
# You must write an algorithm that runs in O(n) time.


def longest_consecutive_sequence(nums: list[int]) -> int:
    num_set = set(nums)
    longest_sequence: int = 0
    # iterate through the set
    for num in num_set:
        # if the number - 1 is not in the set, then it is the start of a new sequence
        if num - 1 not in num_set:
            current_num = num
            current_sequence = 1
            # while the number + 1 is in the set, then it is part of the same sequence
            while current_num + 1 in num_set:
                current_num += 1
                current_sequence += 1
            longest_sequence = max(longest_sequence, current_sequence)

    return longest_sequence

# Solution: We use a set to store the numbers in the array.
# Then we iterate through the set and check if the number - 1 is in the set.
# If it is not, then it is the start of a new sequence. We then check if the number + 1 is in the set.
# If it is, then it is part of the same sequence. We then return the longest sequence.

# Time complexity: O(n))
# Space complexity: O(n)

# Test cases
print(longest_consecutive_sequence([100,4,200,1,3,2])) # output: 4
print(longest_consecutive_sequence([0,3,7,2,5,8,4,6,0,1])) # output: 9