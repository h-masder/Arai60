- 再帰を使わない
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True
        
        node_and_ranges = [(root, None, None)]
        while node_and_ranges:
            node, lower, upper = node_and_ranges.pop()
            if node is None:
                continue
            if lower is not None and node.val <= lower:
                return False
            if upper is not None and upper <= node.val:
                return False

            node_and_ranges.append((node.left, lower, node.val))
            node_and_ranges.append((node.right, node.val, upper))
        return True
```

- 再帰を使う


```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root : Optional[TreeNode]) -> bool:
        def is_valid_BST_helper(node: TreeNode, lower: Optional[int], upper: Optional[int]) -> bool:
            if node is None:
                return True 

            if lower is not None and node.val <= lower:
                return False
            if upper is not None and upper <= node.val:
                return False
            
            return is_valid_BST_helper(node.left, lower, node.val) and is_valid_BST_helper(node.right, node.val, upper)
        
        return is_valid_BST_helper(root, None, None)
```
