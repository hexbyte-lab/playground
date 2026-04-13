from typing import Optional
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def subtreeWithAllDeepest(self, root: Optional[TreeNode]) -> Optional[TreeNode]:
        def dfs(node):
            if not node:
                return (0, None)
            
            left_depth, left_node = dfs(node.left)
            right_depth, right_node = dfs(node.right)
            
            if left_depth > right_depth:
                return (left_depth + 1, left_node)
            elif right_depth > left_depth:
                return (right_depth + 1, right_node)
            else:
                return (left_depth + 1, node)
        
        return dfs(root)[1]
    
"""
Solution:
The solution uses (DFS) approach
to traverse the binary tree
and determine the depth of each subtree.
The key idea is to return both the depth of the subtree
and the node that is the root of the smallest subtree
containing all the deepest nodes.
The dfs function returns a tuple containing:
1. The depth of the subtree rooted at the current node.
2. The node that is the root of the smallest subtree containing all the deepest nodes.
If the left and right subtrees have the same depth,
the current node is the root of the smallest subtree containing all the deepest nodes.
"""
