## 問題
https://leetcode.com/problems/maximum-depth-of-binary-tree/description/

Given the root of a binary tree, return its maximum depth.
A binary tree's maximum depth is the number of nodes along the longest path from the root node down to the farthest leaf node.

Constraints:
The number of nodes in the tree is in the range [0, 104].
-100 <= Node.val <= 100

## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## アプローチ
深さ優先探索や幅優先探索でとけばよさそう。
全nodeに一回アクセスすれば深さはわかるので、どんなやりかたでもいい気がする。
両方の方法で解いてみる。

実行時間はnode数に依存。今回は、最大で10^4。
Pythonの実行ステップを10^7/秒とすると数ミリ秒かかる。


### 幅優先
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0 

        depth = 0
        frontier = [root]
        while frontier:
            next_frontier = []
            for node in frontier:
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            frontier = next_frontier
            depth += 1
        
        return depth
```
ざっとこんな感じ。

```py
        if root is None:
            return 0
```
の箇所はNoneと0のどちらを返すか迷った。
Noneで書いたところexpected valueが0だったので、この問題の要求は0だった。


### 深さ優先
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        
        max_depth = 1
        frontier = [(root, 1)]
        while frontier:
            node, depth= frontier.pop()
            max_depth = max(max_depth, depth)
            if node.left is not None:
                frontier.append((node.left, depth + 1))
            if node.right is not None:
                frontier.append((node.right, depth + 1))
        return max_depth
```
未探索のノードの最大の深さは「全ノード数 − 探索済みノード数」より深くならないので、途中で探索を打ち切ることもできる。
例えば、全ノード数が100のときに深さ51の経路を見つけた場合、残りのノードで到達可能な深さは最大でも49となるため、それ以上探索する必要はない。
ただし、これによって得られる速度改善は最大でも約2倍なので、数行追加して認知負荷をあげるくらいなら、やらなくてよい。


## 他の人のコードを見る。

1) 他の書き方ができるか？
- https://github.com/Manato110/LeetCode-arai60/pull/21/changes#r3085249096
> DFSの方をiterativeに（再帰ではない方法で）書けますか？

これを見て、自分の場合は逆に再帰で書いておくかという気持ちになったので、書く。
**幅優先、再帰**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if root is None:
            return 0
        def explore_tree(nodes: List[TreeNode]) -> int:
            if not nodes:
                return 0
            next_nodes = []
            for node in nodes:
                if node.left is not None:
                    next_nodes.append(node.left)
                if node.right is not None:
                    next_nodes.append(node.right)
            return 1 + explore_tree(next_nodes)
        
        return explore_tree([root])
```

**深さ優先、再帰**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, node: Optional[TreeNode]) -> int:
        if node is None:
            return 0
        
        left_depth = self.maxDepth(node.left)
        right_depth = self.maxDepth(node.right)

        return max(left_depth, right_depth) + 1
```

### コメント
2) 深さ優先に`frontier`という名前を使うかどうか。
- https://github.com/kitano-kazuki/leetcode/pull/24#discussion_r2964278699
- nodes_to_visitとかでもよさそう

3) None判定について
- https://github.com/plushn/SWE-Arai60/pull/21/changes#r2597516998
> if node.left: はNoneを弾く意図だと思いますが、注意深い読み手はspecial method TreeNode.__bool__()がオーバーライドされてないか気になってしまいます。また実際にTreeNode.__bool__()の実装次第ではnode.leftがNoneでなくとも意図せずimplicit falsyが成立しうる点が危ういと感じるので、個人的にはif node.left is not Noneの方が好ましいと感じます。

- 上記の不安に加えて、None判定するところで、`if node.left`と書いてあると、以下の区別ができているか、読み手によっては不安に感じるかもしれないと感じた。
```py
node = []
if not node:
    # 実行される
if node is None:
    # 実行されない
```
