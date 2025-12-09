# Problem: Given an array of integers nums and an integer k, you need to perform the following operations:
# Select an index i and replace nums[i] with nums[i] - 1.
# Return the minimum number of operations required to make the sum of the array divisible by k.


def minimum_operations_to_make_array_sum_divisible_by_k(nums: list[int], k: int) -> int:
    return (sum(nums) % k) if sum(nums) % k != 0 else 0


# Time complexity: O(n)
# Space complexity: O(1)
# Test cases
print(minimum_operations_to_make_array_sum_divisible_by_k([3, 9, 7], 5))  # output: 4
