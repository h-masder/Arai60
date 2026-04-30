各node p に対して以下のチェックを行えばよい
  - 方針
    - p の左部分木をすべて探索して、その最大値が p の値よりも小さくことをチェック
    - p の右部分木をすべて探索して、その最小値が p の値よりも大きいことをチェック

1) コードでの表現方法: 葉から根に上っていくようにnodeを見ていく。再帰で書く。
1-1-1) 再帰で書く方法。float("inf")やfloat("-inf")は個人的には避けたいので使わない（型の違いが気になる。）
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def is_valid_BST_helper(node: Optional[TreeNode]) -> Tuple[bool, List[int]]:
            if node is None:
                return True, []
            
            left_valid, left_ranges = is_valid_BST_helper(node.left)
            right_valid, right_ranges = is_valid_BST_helper(node.right)
            if not (left_valid and right_valid):
                return False, []
            if left_ranges and node.val <= left_ranges[1]:
                return False, []
            if right_ranges and right_ranges[0] <= node.val:
                return False, []
            
            node_ranges = left_ranges + [node.val] + right_ranges
            return True, [min(node_ranges), max(node_ranges)]
            
        return is_valid_BST_helper(root)[0]
```
1-1-2) List[int]の中身が最後まで読まないとわからないのがちょっと嫌なので、先に分かるようにする方法も書いてみる。
```py
class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:
        def is_valid_BST_helper(node: Optional[TreeNode]) -> Tuple[bool, Optional[int], Optional[int]]:
            if node is None:
                return True, None, None
            
            left_valid, left_min, left_max = is_valid_BST_helper(node.left)
            right_valid, right_min, right_max = is_valid_BST_helper(node.right)
            if not left_valid or not right_valid:
                return False, None, None
            if left_max is not None and node.val <= left_max:
                return False, None, None
            if right_min is not None and right_min <= node.val:
                return False, None, None
            
            node_min = left_min if left_min is not None else node.val
            node_max = right_max if right_max is not None else node.val
            return True, node_min, node_max

        return is_valid_BST_helper(root)[0]
```


1-2)  再帰を使わない方法。validを使わずに書ける。
- naoto-iwaseさんのコードと、小田さんのコードがある。
  - https://github.com/naoto-iwase/leetcode/pull/33/changes/BASE..2404c21c24a749b6f871d9030b7df0096beb856d#r2479195403
  - 小田さんのコードは、[最小値、最大値]の扱いを追うのがかなりつらい。ので、そのあたりを改良して書いてみた。
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

        node_and_root_to_leaf = [(root, True)]
        node_and_ranges = {None: []}
        while node_and_root_to_leaf:
            node, root_to_leaf = node_and_root_to_leaf.pop()
            if root_to_leaf:
                node_and_root_to_leaf.append((node, False))
                if node.left is not None:
                    node_and_root_to_leaf.append((node.left, True))
                if node.right is not None:
                    node_and_root_to_leaf.append((node.right, True))
                continue
            else:
                left_ranges = node_and_ranges[node.left]
                right_ranges = node_and_ranges[node.right]
                if left_ranges and node.val <= left_ranges[1]:
                    return False
                if right_ranges and right_ranges[0] <= node.val:
                    return False
                node_ranges = left_ranges + [node.val] + right_ranges
                node_and_ranges[node] = [min(node_ranges), max(node_ranges)]

        return True
```



1-3) 葉ではなく、前から順に見ていく（幅優先を使って）。
- rootから順にみていく幅優先は、今回のように部分木の情報が欲しい場合は、相性が悪い。
- 強引にやるなら、今のnodeに対し、左部分木の最小値と右部分木の最大値を持ってきて、それを使う。
- 結局、最小値と最大値を求めるには、葉まで探索する必要があるので、二度手間。だけど、筋が悪いコード例も書いておくとよいと思うので書く。
- 各nodeに対して、毎回部分木を調べ最小値と最大値を調べる方法。メモリアクセスは最大でn + n - 1 + ... + 1 = n(n + 1) / 2 (n: node数)くらいかかるのでPythonの実行時間を10^7/秒とすると最大数秒かかる。

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
        
        def get_max_of_subtree(node: Optional[TreeNode]) -> Optional[int]:
            if node is None:
                return None
            left_max = get_max_of_subtree(node.left)
            right_max = get_max_of_subtree(node.right)
            
            node_max = node.val
            if left_max is not None:
                node_max = max(left_max, node_max)
            if right_max is not None:
                node_max = max(right_max, node_max)
            return node_max
        
        def get_min_of_subtree(node: Optional[TreeNode]) -> Optional[int]:
            if node is None:
                return None
            left_min = get_min_of_subtree(node.left)
            right_min = get_min_of_subtree(node.right)
            
            node_min = node.val
            if left_min is not None:
                node_min = min(left_min, node_min)
            if right_min is not None:
                node_min = min(right_min, node_min)
            return node_min

        not_visited_nodes = [root]
        while not_visited_nodes:
            node = not_visited_nodes.pop()
            if node.left is not None:
                left_max = get_max_of_subtree(node.left)
                if left_max is not None and node.val <= left_max:
                    return False
                not_visited_nodes.append(node.left)
            if node.right is not None:
                right_min = get_min_of_subtree(node.right)
                if right_min is not None and right_min <= node.val:
                    return False
                not_visited_nodes.append(node.right)
            
        return True
```
