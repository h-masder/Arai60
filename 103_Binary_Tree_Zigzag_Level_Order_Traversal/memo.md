## 問題
https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/description/

Given the root of a binary tree, return the zigzag level order traversal of its nodes' values. (i.e., from left to right, then right to left for the next level and alternate between).

Constraints:
The number of nodes in the tree is in the range [0, 2000].
-100 <= Node.val <= 100

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
- (102. Binary Tree Level Order Traversal)との違いは、レベルごとの値の並び順のみである。
- 偶数レベルでは左から右、奇数レベルでは右から左に値を並べることで、zigzag 順を実現する。


## 補足
- 前問(102. Binary Tree Level Order Traversal)へのコメントありがとうございます。
- そちらのコメントを見る前に解いてしまったため、コメントを反映したコードはstep3で書きました。

**実行時間の見積もり**

各ノードに高々一回のメモリアクセス。各メモリアクセスでは定数ステップなので、そう実行ステップは2*10^3くらい
Pythonの実行時間が10^7/秒だとすると、数百ns～数msくらいかかる。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzag_level_order(self, root: Optional[TreeNode]) -> List[List[int]]: 
        if not root:
            return []
        
        zigzag_order_values = []
        not_visited_nodes = [(root)]
        level = 0
        while not_visited_nodes:
            next_visited_nodes = []
            current_order = []
            for node in not_visited_nodes:
                current_order.append(node.val)
                if node.left is not None:
                    next_visited_nodes.append(node.left)
                if node.right is not None:
                    next_visited_nodes.append(node.right)

            if level % 2 == 0:
                zigzag_order_values.append(current_order)
            else:
                zigzag_order_values.append(current_order[::-1])
            not_visited_nodes = next_visited_nodes
            level += 1

        return zigzag_order_values
```

- ここまでで17分
- levelをどう管理するか、どう逆順に整形するかを考えて、手間取った。


- 深さ優先なら、最後にまとめてlevelが奇数のものを逆順にするのが楽かな？

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzag_level_order(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        node_and_levels = [(root, 0)]
        level_values = []
        while node_and_levels:
            node, level = node_and_levels.pop()
            while len(level_values) <= level:
                level_values.append([])
            level_values[level].append(node.val)

            if node.right is not None:
                node_and_levels.append((node.right, level + 1))
            if node.left is not None:
                node_and_levels.append((node.left, level + 1))
        
        for i in range(len(level_values)):
            if i % 2 == 1:
                level_values[i].reverse()
                
        return level_values
        
```

- ただし、上記のコードだと読みにくいかもしれない。読者は「どこで zigzag にしているのだろう？」と思いながら読み進めるものの、前半ではその処理が現れず、最後の reverse で初めて zigzag を実現していることに気づく。
- 処理の役割ごとに内部関数として分離し、「どこで何をしているか」を明示した方が、コードの可読性は向上する気がする。


```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzag_level_order(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        def generate_level_order_values(node_and_levels: List[Tuple[TreenNode, int]]) -> List[List[int]]:
            level_values = []
            while node_and_levels:
                node, level = node_and_levels.pop()
                while len(level_values) <= level:
                    level_values.append([])
                level_values[level].append(node.val)

                if node.right is not None:
                    node_and_levels.append((node.right, level + 1))
                if node.left is not None:
                    node_and_levels.append((node.left, level + 1))
            return level_values
        
        def transform_zigzag_order(level_values: List[List[int]]):
            for i in range(len(level_values)):
                if i % 2 == 1:
                    level_values[i].reverse()
            return level_values

        level_values = generate_level_order_values([(root, 0)])
        return transform_zigzag_order(level_values)

```

## 他の人の解答を見る。コメントを残す。

- 最後にreverseする方法ではなく、left_to_right と right_to_leftの交互にstackを積んでいく
  - https://github.com/Manato110/LeetCode-arai60/pull/27 の step3
  - 練習はしておく。若干ややこしいので、実務でこういう実装は避けるかもしれない。
  
- 最後にreverseする方法ではなく、逐次的に処理をする方法
  - https://github.com/Yuto729/LeetCode_arai60/pull/32/changes#diff-12a9ab9cc57136608e7370d97a9fc93f941773d5c591a846a98b64f72e54062dR74-R76
  - 探索は常に左からだが、level が奇数のときは、リストを逆順につくっていく(でてきたnode.valを先頭に追加していく)。
  - 個人的には、リストのほうが好みかもしれない。
  - https://github.com/tom4649/Coding/pull/26#discussion_r2952353928

- zigzagの判断に、偶奇判定を使うのか。bool値反転で対処するのか。
  - https://github.com/kitano-kazuki/leetcode/pull/27/changes#r2980278314
  - 個人的にはどっちでもいいかな...。
  - rootのdepthを"0"ととらえる人と"1"ととらえる人がいる。
    - https://github.com/tom4649/Coding/pull/26#discussion_r2961354227
    - だとするとbool値のほうがいいのか。と思いつつ、どっちでもいいかなとは思う。

- リストの反転にreverseを使うか。[::-1]を使うか。
  - https://github.com/kitano-kazuki/leetcode/pull/27/changes#r2980288236
  - > https://github.com/kitano-kazuki/leetcode/pull/27/changes#r2980288236
  - > C++ はコピーうるさめですが、Python は細かいことをいってもしょうがないところもありますね。いずれにせよどれくらい遅いかは定量的に考えておきましょう。
  - insert() と reverse() の違いには着目していたが、[::-1] と reverse() を見たときに、その違いを確認しようという意識はなかった。

- step3
- 自分の書いたコードに加え、https://github.com/Manato110/LeetCode-arai60/pull/27 の step3を練習する。
- また。前問でもらったコメントを反映する（変数名などを変更する）。

- **幅優先**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        not_visited_nodes = [root]
        left_to_right = True
        level_to_values = []
        while not_visited_nodes:
            next_visited_nodes = []
            values = []
            for node in not_visited_nodes:
                values.append(node.val)
                if node.left is not None:
                    next_visited_nodes.append(node.left)
                if node.right is not None:
                    next_visited_nodes.append(node.right)
            if left_to_right:
                level_to_values.append(values)
            else:
                level_to_values.append(values[::-1])
            not_visited_nodes = next_visited_nodes
            left_to_right = not left_to_right

        return level_to_values
```
- **深さ優先**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []

        def generate_left_to_right_order_values(node_and_levels: List[Tuple[TreeNode, int]]) -> List[List[int]]:
            level_to_values = []
            while node_and_levels:
                node, level = node_and_levels.pop()
                while len(level_to_values) <= level:
                    level_to_values.append([])
                level_to_values[level].append(node.val)
                
                if node.right is not None:
                    node_and_levels.append((node.right, level + 1))
                if node.left is not None:
                    node_and_levels.append((node.left, level + 1))

            return level_to_values
        
        def transform_zigzag_order(level_to_values: List[List[int]]) -> List[List[int]]:
            right_to_left = False
            for i in range(len(level_to_values)):
                if right_to_left:
                    level_to_values[i].reverse()
                right_to_left = not right_to_left
            return level_to_values
        
        level_to_values = generate_left_to_right_order_values([(root, 0)])
        return transform_zigzag_order(level_to_values)
```

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        def generate_left_to_right_order_values(node_and_levels: List[Tuple[TreeNode, int]]) -> List[List[int]]:
            level_to_values = []
            while node_and_levels:
                node, level = node_and_levels.pop()
                while len(level_to_values) <= level:
                    level_to_values.append([])
                level_to_values[level].append(node.val)
                
                if node.right is not None:
                    node_and_levels.append((node.right, level + 1))
                if node.left is not None:
                    node_and_levels.append((node.left, level + 1))


            return level_to_values
        
        def transform_zigzag_order(level_to_values: List[List[int]]) -> List[List[int]]:
            left_to_right = True
            for i in range(len(level_to_values)):
                if not left_to_right:
                    level_to_values[i].reverse()
                left_to_right = not left_to_right
            return level_to_values
        
        level_to_values = generate_left_to_right_order_values([(root, 0)])
        return transform_zigzag_order(level_to_values)
```

- **https://github.com/Manato110/LeetCode-arai60/pull/27 の step3**

- 後でリストを逆順にする代わりに、最初から逆順でstackに積むという考え方
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def zigzagLevelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root:
            return []
        
        not_visited_nodes = [root]
        left_to_right = True
        level_to_values = []
        while not_visited_nodes:
            next_visited_nodes = []
            values = []
            while not_visited_nodes:
                node = not_visited_nodes.pop()
                values.append(node.val)
                if left_to_right:
                    if node.left is not None:
                        next_visited_nodes.append(node.left)
                    if node.right is not None:
                        next_visited_nodes.append(node.right)
                else:
                    if node.right is not None:
                        next_visited_nodes.append(node.right)
                    if node.left is not None:
                        next_visited_nodes.append(node.left)

            level_to_values.append(values)
            not_visited_nodes = next_visited_nodes
            left_to_right = not left_to_right

        return level_to_values
        
```
