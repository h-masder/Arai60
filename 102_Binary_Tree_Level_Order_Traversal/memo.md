## 問題
https://leetcode.com/problems/binary-tree-level-order-traversal/description/

Given the root of a binary tree, return the level order traversal of its nodes' values. (i.e., from left to right, level by level).

Constraints:
The number of nodes in the tree is in the range [0, 2000].
-1000 <= Node.val <= 1000

## 進め方

- (step1) 自分で考える。面接を意識してどういったアプローチで書くのか記述する。
  - 書く前に時間計算量を見積もる。
    - https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
  - 時間制限はEasyなら15分、mediumなら30分(アプローチや、実行時間を書くことも含む)。
- (step2) 他の人のコードを見て(レビューして)、自分のコードと比較して修正する。さらに、見たコードに対してコメントを残す。レビューの仕方は以下を参考にする。
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
  　　- コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
- (step3) エラーをはかずに3回書けるようにする。

## アプローチ

- やることはそのまま。
  - 同じlevelのものを同じ配列にいれて保持するだけ。

**実行時間の見積もり**
- すべてのnodeに高々一回アクセスする。各nodeに対する処理は定数ステップなので、実行ステップの合計は、2*10^3
- Pythonの実行ステップが10^7/秒とすると数百ns~数msくらいかかる。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        level_values = []
        frontier = [(root)]
        while frontier:
            next_frontier = []
            current_level = []
            for node in frontier:
                current_level.append(node.val)
                if node.left is not None:
                    next_frontier.append(node.left)
                if node.right is not None:
                    next_frontier.append(node.right)
            frontier = next_frontier
            level_values.append(current_level)
        return level_values
```

アプローチや実行時間の記述、処理の見直しを含めて9分11秒。
この問題の変形は、次の問題を解けばよさそうなので、スキップ。


## 他の人の解答を見る。解答を見たらコメントを残す。


- nodeのlevelを管理しながら、リストを作っていく方法
  - https://github.com/rimokem/arai60/pull/26 の step2
  - そんなに好きな書き方ではないが、練習で書いてみる上記のPRでは、再帰をつかって書いてみるので、自分は再帰なしで書いてみる
  - この方法も、実行時間は最初の解答と大差なし。
    - すべてのnodeに高々一回アクセスする。各nodeに対する処理は定数ステップなので

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        level_values = []
        not_visited_nodes = [(root, 0)]
        while not_visited_nodes:
            node, level = not_visited_nodes.pop()
            while len(level_values) <= level:
                level_values.append([])
            level_values[level].append(node.val)

            if node.right is not None:
                not_visited_nodes.append((node.right, level + 1))
            if node.left is not None:
                not_visited_nodes.append((node.left, level + 1))

        return level_values
```

- 気を付けること
  1) appendする順番。right->leftの順にいれないと、取り出すときにleft->rightとならず、順序が崩れる。
  2) if vs while (https://github.com/Yuto729/LeetCode_arai60/pull/31 を読んでこの議論がされていたことを知った。)

    - 気にしているのは以下のコード。
```py
            if len(level_values) == level:
                level_values.append([])
```
- https://discord.com/channels/1084280443945353267/1200089668901937312/1211248049884499988
>私は、while だと思っていて、上から読んでいくと、「level が大きくて nodes_ordered_by_level が足りない場合、足りるように拡張します。そして、拡張した場所に書き込みます。」(読んでいくと、あとから、足りないことがあったとしても1段であることが他のところから分かる。)
> 「level が大きくて nodes_ordered_by_level が足りない場合、1段だけ拡張します。そして、level 番目に書き込みます。(書き込めなかったら IndexError が投げられます。)」(読んでいくと、1段だけしか拡張しなくても、level 番目が準備されているので例外はないことが分かる。)

>というふうに読めます。どっちが読み手にとっていいですか。

- 私はこれを読んでwhileがいいなと思った。読み手に「大丈夫かな?」と思わせないのは大事。実際、他の人のコードをみたときに、大丈夫なのか検証した。

- 以下のPRを読んだ。想定の範囲内かな。
- https://github.com/Yuto729/LeetCode_arai60/pull/31
- https://github.com/Manato110/LeetCode-arai60/pull/26
- https://github.com/rimokem/arai60/pull/26
- https://github.com/kitano-kazuki/leetcode/pull/26/changes


- step3は、上の二つに加えて、再帰バージョンで3回エラーをださずに書く
