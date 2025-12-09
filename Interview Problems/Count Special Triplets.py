# Problem: You are given an array of integers nums.
# You need to find the number of special triplets in the array.
# A special triplet is a triplet (i, j, k) such that:
# 1. i < j < k
# 2. nums[i] * 2 = nums[j]
# 3. nums[j] * 2 = nums[k]

# Example:
# Input: nums = [1, 2, 2, 4, 8]
# Output: 2
# Explanation: The special triplets are (1, 2, 4) and (2, 2, 4).


def specialTriplets(nums) -> int:
    seen: dict[int, int] = {}
    will_see: dict[int, int] = {}


    for num in nums:
        seen[num] = seen.get(num, 0) + 1

    count: int = 0
    for i in range(len(nums)):
        target = nums[i] * 2
        # count the left boxes with target candies
        left_count = will_see.get(target, 0)
        will_see[nums[i]] = will_see.get(nums[i], 0) + 1
        # count the right boxes with target candies
        # we subtract the left count from the total count to get the right count
        right_count = seen.get(target, 0) - will_see.get(target, 0)
        count += left_count * right_count

    return count % (10**9 + 7)

# Solution: We use a dictionary to store the numbers we have seen so far
# and the numbers we will see next.
# We then iterate through the array and count the number of special triplets.


# Time Complexity: O(n)
# Space Complexity: O(n)


print(specialTriplets([8,4,2,8,4]))  # output: 2
