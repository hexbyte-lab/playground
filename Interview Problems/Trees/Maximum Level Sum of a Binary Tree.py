r"""
Maximum Level Sum of a Binary Tree
Source: https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/

Levels are numbered from 1 at the root. Return the smallest level number whose
node values sum to the maximum among all levels.

Example:
        1
       / \
      7   0          level 1 sum = 1
     / \             level 2 sum = 7
    7  -8            level 3 sum = -1   -> max is level 2
    Output: 2

Approach:
    DFS while accumulating each level's sum in a map keyed by depth, then return
    the lowest level number achieving the maximum sum.

Complexity: Time O(n) | Space O(h)   # h = tree height (levels stored)
"""

from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def maxLevelSum(self, root: Optional[TreeNode]) -> int:
        level_sums: dict[int, int] = {}

        def dfs(node: Optional[TreeNode], level: int) -> None:
            if not node:
                return
            level_sums[level] = level_sums.get(level, 0) + node.val
            dfs(node.left, level + 1)
            dfs(node.right, level + 1)

        dfs(root, 1)

        best_level = 1
        best_sum = float("-inf")
        for level in sorted(level_sums):
            if level_sums[level] > best_sum:
                best_sum = level_sums[level]
                best_level = level
        return best_level


if __name__ == "__main__":
    #       1
    #      / \
    #     7   0
    #    / \
    #   7  -8
    root = TreeNode(1, TreeNode(7, TreeNode(7), TreeNode(-8)), TreeNode(0))
    print(Solution().maxLevelSum(root))  # 2
