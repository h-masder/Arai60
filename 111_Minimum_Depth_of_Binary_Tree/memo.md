## 問題
https://leetcode.com/problems/minimum-depth-of-binary-tree/description/

Given a binary tree, find its minimum depth.
The minimum depth is the number of nodes along the shortest path from the root node down to the nearest leaf node.
Note: A leaf is a node with no children.

Constraints:
The number of nodes in the tree is in the range [0, 10^5].
-1000 <= Node.val <= 1000

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## アプローチ
幅優先でやるのがよさそう。
葉を見つけたらそこまでのdepthを返す。

**実行時間の見積もり**
最大でも全ノードへのアクセスで済む(10^5回)。
Pythonの実行ステップを10^7/秒とすると、数十ミリ秒くらい

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        
        frontier = [(root, 1)]
        while frontier:
            next_frontier = []
            for node, depth in frontier:
                if node.left is None and node.right is None:
                    return depth
                if node.left is not None:
                    next_frontier.append((node.left, depth + 1))
                if node.right is not None:
                    next_frontier.append((node.right, depth + 1))
            frontier = next_frontier
```
再帰で書くなら以下のような感じ
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        def explore_tree(nodes: List[TreeNode]) -> int:
            next_frontier = []
            for node in nodes:
                if node.left is None and node.right is None:
                    return 0
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            return 1 + explore_tree(next_frontier)

        return 1 + explore_tree([root])
```

- 一応深さ優先で書くならこんな感じ
　- 葉が見つかり次第、returnするのに対し、すべてのノードにアクセスするので、幅優先より遅くなる。
　- 一番時間差が縮まるのは完全二分木だが、それでも幅優先（メモリアクセスはだいたい(全ノード数)/2くらい）に比べて深さ優先（メモリアクセスは(全ノード数)）のほうが二倍くらい遅い
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0

        min_depth = float('inf')
        node_to_visit = [(root, 1)]
        while node_to_visit:
            node, depth = node_to_visit.pop()
            if node.left is None and node.right is None:
                min_depth = min(min_depth, depth)
            if node.left is not None:
                node_to_visit.append((node.left, depth + 1))
            if node.right is not None:
                node_to_visit.append((node.right, depth + 1))

        return min_depth
```
- float('inf')は若干気持ち悪いが、まあしかたないのかな。代替案としては、NUM_ALL_NODES = 100000のように定義しておくこと。


- 再帰あり
　- まず葉ノードまで到達し、そこから親ノードへ戻りながら最小の深さを求めていく。
　- 各ノードでは、左右の部分木の深さを比較し、小さい方を採用する。
　- ただし、片方の子ノードが存在しない場合は、その方向には進めないため、存在するノードを採用する。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def minDepth(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        
        if node.left is None:
            return 1 + self.minDepth(node.right)
        if node.right is None:
            return 1 + self.minDepth(node.left)
        
        return 1 + min(self.minDepth(node.left), self.minDepth(node.right))
```



## 他の方のコードを見る。

1) 場合分けで冗長な記述にならないように気を付ける。
- https://github.com/olsen-blue/Arai60/pull/22#discussion_r1929807128

2) 他の人のコードを見たが想定の範囲内。ただ、再帰はちょっと読み慣れていない感じはする。
- https://github.com/rimokem/arai60/pull/22
- https://github.com/Manato110/LeetCode-arai60/pull/22
- https://github.com/hemispherium/LeetCode_Arai60/pull/21/changes
- https://github.com/yumyum116/LeetCode_Arai60/pull/19
- https://github.com/kitano-kazuki/leetcode/pull/22
