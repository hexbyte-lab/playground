"""
You are given an n x n integer matrix.
You can do the following operation any number of times:

Choose any two adjacent elements of matrix and multiply each of them by -1.
Two elements are considered adjacent if and only if they share a border.

Your goal is to maximize the summation of the matrix's elements. Return the maximum sum of the matrix's elements using the operation mentioned above.

Input: matrix = [[1,2,3],[-1,-2,-3],[1,2,3]]
Output: 16
Explanation: We can follow the following step to reach sum equals 16:
- Multiply the 2 last elements in the second row by -1.

"""

from typing import List


def maxMatrixSum(matrix: List[List[int]]) -> int:
    n = len(matrix)
    negative_count = 0
    min_abs_val = float("inf")
    total_sum = 0

    for i in range(n):
        for j in range(n):
            val = matrix[i][j]
            total_sum += abs(val)
            if val < 0:
                negative_count += 1
            min_abs_val = min(min_abs_val, abs(val))

    if negative_count % 2 == 0:
        return total_sum
    else:
        return total_sum - 2 * int(min_abs_val)


"""
Solution: 
we count the number of negative elements in the matrix.
If the count is even, we can make all elements positive.

If the count is odd, we need to leave one negative element,
and we should leave the one with the smallest absolute value.

if the count of negative numbers is odd,
we subtract twice the smallest absolute value from the total sum of absolute values.
else, we return the total sum of absolute values directly.
"""

print(maxMatrixSum([[1, 2, 3], [-1, -2, -3], [1, 2, 3]]))  # Output: 16
print(maxMatrixSum([[-1, -1], [-1, -1]]))  # Output: 4
