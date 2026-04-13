from typing import List


def findDisappearedNumbers(nums: List[int]) -> List[int]:
    n = len(nums)
    for i in range(n):
        index = abs(nums[i]) - 1
        if nums[index] > 0:
            nums[index] = -nums[index]

    result = []
    for i in range(n):
        if nums[i] > 0:
            result.append(i + 1)

    return result

"""
Solution:
We iterate through the array and for each number,
we mark the index corresponding to that number as negative.
If a number x is present in the array,
we mark the number at index x-1 as negative.
After marking, we iterate through the array again.
The indices which have positive values
correspond to the numbers that are missing from the array.
"""

print(findDisappearedNumbers([4, 3, 2, 7, 8, 2, 3, 1]))  # Output: [5,6]
