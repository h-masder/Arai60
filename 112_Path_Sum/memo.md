## 問題
https://leetcode.com/problems/path-sum/description/

Given the root of a binary tree and an integer targetSum, return true if the tree has a root-to-leaf path such that adding up all the values along the path equals targetSum.
A leaf is a node with no children.

Constraints:
The number of nodes in the tree is in the range [0, 5000].
-1000 <= Node.val <= 1000
-1000 <= targetSum <= 1000

## 進め方

- (step1) 自分で考える。面接を意識してどういったアプローチで書くのか記述する。書く前に時間計算量を見積もる。時間制限はEasyなら15分、mediumなら30分(アプローチや、実行時間を書くことも含む)。
  - https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
- (step2) 他の人のコードを見て(レビューして)、自分のコードと比較して修正する。さらに、見たコードに対してコメントを残す。レビューの仕方は以下を参考にする。
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  　　- コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
- (step3) エラーをはかずに3回書けるようにする。

## アプローチ

- 入力はroot: TreeNode, targetSum: int、
- 出力はTrue or False: bool
- エッジケースとして、root = []なら、Falseを返す。
- 思いつくアプローチは二つ：
  - [1] root-to-leafを一つずつ見ていって、nodeの値を合計していき、leafにたどりついたとき、targetSumと同じであるかみる
    - leafにたどりつかなくても途中でtargetSumを超えたときは、それ以上は探索しなくてもよい。-> nodeの値がマイナスがあるので、途中で引き返すのはダメであることに気づいた。
  - [2] 各深さを並列で見ていき、途中でleafにたどりついたものがtargetSuｍと同じかどうか。

- どちらでもよさそう。両方書いてみる。
**実行時間の見積もり**
どんなにかかっても、各nodeは高々一回のアクセス。各アクセスは定数ステップの処理なので、そう実行ステップはだいたいnode数(<=5*10^3)と同じくらい。10^4くらいかな
Pythonの実行ステップが10^7/秒だとすると、最大でも数ミリかかる程度

- [1] の解法
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        
        not_visited_nodes = [(root, 0)]
        while not_visited_nodes:
            node, total = not_visited_nodes.pop()
            total += node.val
            if node.left is None and node.right is None:
                if targetSum == total:
                    return True
            if node.left is not None:
                not_visited_nodes.append((node.left, total))
            if node.right is not None:
                not_visited_nodes.append((node.right, total))

        return False
```

- ここまでで14分(アプローチの記述、コードの再チェックも含む)
- 15分を超えそうだが、延長してもう一つのアプローチも書く。


- [2] の解法
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        
        not_visited_nodes = [(root, 0)]
        while not_visited_nodes:
            next_visited_nodes = []
            for node, total in not_visited_nodes:
                total += node.val
                if node.left is None and node.right is None:
                    if targetSum == total:
                        return True
                if node.left is not None:
                    next_visited_nodes.append((node.left, total))
                if node.right is not None:
                    next_visited_nodes.append((node.right, total))
            not_visited_nodes = next_visited_nodes
        return False
```

- ここまでで18分。

- 再帰のパターンも書いてみた。考え方は同じ。
- コードの表現として違うのは、targetSumの値を減算していき、0になったらTrueを返すということ。
  - ただし、再帰だからこう書かなくてはいけないわけではなく、単にバリエーションとして思いついたので書いてみた。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False

        if root.left is None and root.right is None:
            if targetSum - root.val == 0:
                return True

        found = False
        if root.left is not None:
            found = self.hasPathSum(root.left, targetSum - root.val)
        if root.right is not None and not found:
            found = self.hasPathSum(root.right, targetSum - root.val)
        return found
```

- この書き方だと、エッジケースが何度も評価されて見にくいのと、targetSumが書き換わっているので、内部関数で書いたほうが良いかもしれない。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: Optional[TreeNode], targetSum: int) -> bool:
        if not root:
            return False
        def hasPathSum_helper(node: TreeNode, targetSum: int) -> bool:
            value = targetSum - node.val
            if node.left is None and node.right is None:
                if value == 0:
                    return True

            found = False
            if node.left is not None:
                found = hasPathSum_helper(node.left, value)
            if node.right is not None and not found:
                found = hasPathSum_helper(node.right, value)
            return found

        return hasPathSum_helper(root, targetSum)
```


## あり得る追加の質問
- 以下のように変更してといわれるかもしれない。
  - Please return **a list of all root-to-leaf paths** such that adding up all the values along the path equals targetSum.
    - 経路を葉までたどったときの合計がtargetSumと一緒になった経路をすべて返すという問題。
- 入力は前問と同じにする。出力はnodeの値のリスト(List[List[int]])とする。
- pathがなければ、[]を返すとする。

- たどったnodeの値のリストと合計を状態で保持しながらたどっていき、辿り着いたら, listに入れる。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getPathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if not root:
            return []
        
        paths = []
        not_visited_nodes = [([root.val], root, 0)]
        while not_visited_nodes:
            path, node, total = not_visited_nodes.pop()
            total += node.val
            if node.left is None and node.right is None:
                if targetSum == total:
                    paths.append(path)
            if node.left is not None:
                not_visited_nodes.append(([node.left.val] + path, node.left, total))
            if node.right is not None:
                not_visited_nodes.append(([node.right.val] + path, node.right, total))
        return paths
```
- 見つかったらleafからrootにかけて経路を構築していく。再帰で書ける？
  - 子から結果が返ってきたとき、リストがあれば、そこ自分のnodeを追加して上に返せばよさそう。
  - こちらは、うまく書けず、LLMの助けをかりて書いた。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def getPathSum(self, root: Optional[TreeNode], targetSum: int) -> List[List[int]]:
        if not root:
            return []

        def getPathSum_helper(node: TreeNode, target: int) -> List[List[int]]:
            value = target - node.val
            if node.left is None and node.right is None:
                if value == 0:
                    return [[node.val]]
                else:
                    return []

            paths = []
            if node.left is not None:
                for path in getPathSum_helper(node.left, value):
                    paths.append(path + [node.val]) 
            if node.right is not None:
                for path in getPathSum_helper(node.right, value):
                    paths.append(path + [node.val])

            return paths

        return getPathSum_helper(root, targetSum)

```
- うまく書けなかったのは、`for path in getPathSum_helper(node.left, target - node.val):`の箇所。
  - leafから空リスト([])が返ってきたときにその扱いに困ったが、上記のように書けばうまく対処できる。
  - この書き方は慣れておきたい。

## 他の人のコードを読む(見た解答にコメントも残す)
- https://github.com/rimokem/arai60/pull/25
- https://github.com/Manato110/LeetCode-arai60/pull/25
- https://github.com/yumyum116/LeetCode_Arai60/pull/22
- https://github.com/kitano-kazuki/leetcode/pull/25
- どれも想定の範囲内に感じた。




- 他の人の解答を見て改善し、全部をミスなく3回書く。改善したところは、例えば、再帰を使わない深さ優先探索は以下のコメントアウトの部分。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def hasPathSum(self, root: TreeNode | None, targetSum: int) -> bool:
        if not root:
            return False
        
        not_visited_nodes = [(root, root.val)] # 一行にまとめる
        while not_visited_nodes:
            node, total = not_visited_nodes.pop()
            if node.left is None and node.right is None:
                if total == targetSum:
                    return True
                continue # continueを追加
            if node.left is not None:
                not_visited_nodes.append((node.left, total + node.left.val))
            if node.right is not None:
                not_visited_nodes.append((node.right, total + node.right.val))
                
        return False
```
