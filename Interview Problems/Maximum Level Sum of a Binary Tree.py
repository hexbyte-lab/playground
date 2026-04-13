


from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right
class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        # a dictionary to store the sum of each level
        level_sums: dict = {}
        def dfs(node, level):
            if not node:
                return
            level_sums[level] = level_sums.get(level, 0) + node.val
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)
        dfs(root, 1)

        # find the smallest level with the maximum sum
        max_sum = float('-inf')
        min_level = float('inf')
        
        for level, sum in level_sums.items():
            if sum > max_sum or (sum == max_sum and level < min_level):
                max_sum = sum
                min_level = level
        
        return min_level
        
        