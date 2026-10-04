r"""
Smallest Subtree with all the Deepest Nodes
Source: https://leetcode.com/problems/smallest-subtree-with-all-the-deepest-nodes/

Return the root of the smallest subtree that contains every one of the tree's
deepest nodes.

Example:
        1
       / \
      2   3
         / \
        4   5      deepest nodes are 4 and 5
    Output: node 3 (their lowest common ancestor)

Approach:
    A single DFS returns, for each node, (depth of its subtree, root of the
    smallest subtree holding that subtree's deepest nodes). If the left side is
    deeper, propagate the left answer; if the right side is deeper, propagate the
    right answer; if they tie, the current node is the answer.

Complexity: Time O(n) | Space O(h)   # h = recursion depth
"""

from typing import Optional, Tuple


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node: Optional[TreeNode]) -> Tuple[int, Optional[TreeNode]]:
            if not node:
                return (0, None)

            left_depth, left_node = dfs(node.left)
            right_depth, right_node = dfs(node.right)

            if left_depth > right_depth:
                return (left_depth + 1, left_node)
            if right_depth > left_depth:
                return (right_depth + 1, right_node)
            return (left_depth + 1, node)

        return dfs(root)[1]


if __name__ == "__main__":
    #       1
    #      / \
    #     2   3
    #        / \
    #       4   5
    root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
    answer = Solution().subtreeWithAllDeepest(root)
    print(answer.val if answer else None)  # 3
