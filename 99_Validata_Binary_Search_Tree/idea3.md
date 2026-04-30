- inorder

- 再帰なし、バリエーション1
```py
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        if root is None:
            return True

        nodes = []
        def explore_left_nodes(node: Optional[TreeNode]) -> None:
            while node is not None:
                nodes.append(node)
                node = node.left
        explore_left_nodes(root)
        previous_value = None
        while nodes:
            node = nodes.pop()
            if previous_value is not None and node.val <= previous_value:
                return False
            previous_value = node.val
            
            explore_left_nodes(node.right)
        
        return True
```
- 再帰なし、バリエーション2
```py
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        node_and_visited = [(root, False)]
        previous_value = None

        while node_and_visited:
            node, visited = node_and_visited.pop()
            if node is None:
                continue
            if visited:
                if previous_value is not None and node.val <= previous_value:
                    return False
                previous_value = node.val
            else:
                node_and_visited.append((node.right, False))
                node_and_visited.append((node, True))
                node_and_visited.append((node.left, False))

        return True
```
- 再帰バージョン
```py
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def is_valid_BST_helper(node: Optional[TreeNode], previous_value: Optional[int]) -> Tuple[bool, Optional[int]]:
            if node is None:
                return True, previous_value

            valid, previous_value = is_valid_BST_helper(node.left, previous_value)
            if not valid:
                return False, previous_value

            if previous_value is not None and node.val <= previous_value:
                return False, previous_value
            previous_value = node.val

            valid, previous_value = is_valid_BST_helper(node.right, previous_value)
            if not valid:
                return False, previous_value

            return True, previous_value
        return is_valid_BST_helper(root, None)[0]
```
`nonlocal`を使うのが嫌だったので、previous_valueを引数や戻り値に入れたが、何度も出てきて見づらいかもしれない。
