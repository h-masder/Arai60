## 進め方

- 自分で考える。書く前に時間計算量を見積もる(https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324)。
- エラーをはかずに3回解くようになるまで書いてみる。
- 他の人のコードを見て、自分のコードと比較して修正する。

## 考え方

- 両方を同時にみて探索していきながら、nodeを作成していく。
- すべてのnodeを見る必要があるので、幅優先でも深さ優先でも実行時間に大した差はない。
- 探索中、両方のnodeがあれば合計をvalに持つnodeを作成する、どちらかがNoneなら、片方の値をいれる。両方ともなくなったら、その経路の探索は終了
- 実装上のポイントは、片方だけになった後の探索。Noneになったほうのleftもrightもないので、参照しないようにする。

- 気を付けること：入力は破壊しない実装にすること。

- **実行時間の見積もり**
- The number of nodes in both trees is in the range [0, 2000].
- 全nodeへのアクセスは2*10^3
- Pythonの実行時間が10^7/秒とすると、最大で数ミリ程度

以下のコードは未完成。
- **幅優先**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1

        merged_root = TreeNode()
        frontier = [(root1, root2, merged_root)]
        while frontier:
            next_frontier = []
            for node1, node2, merged_node in frontier:
                if node1 is not None and node2 is not None:
                    merged_node.val = node1.val + node2.val
                elif node1 is not None:
                    merged_node.val = node1.val
                elif node2 is not None:
                    merged_node.val = node2.val
                
                #次を探す


            frontier = next_frontier
        
        return merged_root
```
- ここまで書いて、「次の候補を探す」書き方がわからず他の人の解答を見た。

- https://github.com/rimokem/arai60/pull/23/changes
 -以下のようなsnippetを拾った。
```py
            left1 = node1.left if node1 is not None else None
            left2 = node2.left if node2 is not None else None
            right1 = node1.right if node1 is not None else None
            right2 = node2.right if node2 is not None else None
```

- 上記を使えば、書けそう。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1

        merged_root = TreeNode()
        frontier = [(root1, root2, merged_root)]
        while frontier:
            next_frontier = []
            for node1, node2, merged_node in frontier:
                if node1 is not None and node2 is not None:
                    merged_node.val = node1.val + node2.val
                elif node1 is not None:
                    merged_node.val = node1.val
                elif node2 is not None:
                    merged_node.val = node2.val
                
                #次を探す
                left1 = node1.left if node1 is not None else None
                left2 = node2.left if node2 is not None else None
                if left1 is not None or left2 is not None:
                    merged_node.left = TreeNode()
                    next_frontier.append((left1, left2, merged_node.left))
                right1 = node1.right if node1 is not None else None
                right2 = node2.right if node2 is not None else None
                if right1 is not None or right2 is not None:
                    merged_node.right = TreeNode()
                    next_frontier.append((right1, right2, merged_node.right))

            frontier = next_frontier
        
        return merged_root
```

- 深さ優先で書くなら以下のような感じ。

- **深さ優先**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1

        merged_root = TreeNode()
        frontier = [(root1, root2, merged_root)]
        while frontier:
            node1, node2, merged_node = frontier.pop()
            if node1 is not None and node2 is not None:
                merged_node.val = node1.val + node2.val
            elif node1 is not None:
                merged_node.val = node1.val
            elif node2 is not None:
                merged_node.val = node2.val
            
            #次を探す
            right1 = node1.right if node1 is not None else None
            right2 = node2.right if node2 is not None else None
            if right1 is not None or right2 is not None:
                merged_node.right = TreeNode()
                frontier.append((right1, right2, merged_node.right))
            left1 = node1.left if node1 is not None else None
            left2 = node2.left if node2 is not None else None
            if left1 is not None or left2 is not None:
                merged_node.left = TreeNode()
                frontier.append((left1, left2, merged_node.left))
        
        return merged_root
```


- もう少し自力でバリエーションを追加する。
  - 深さ優先（再帰）
  - 幅優先（再帰）
  - 入力を書き換える方法
- 加えて、もう少し整理できないか考えた。merged_node.valは一つにまとめられる

- **深さ優先(再帰)**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1
        
        merged_root = TreeNode()
        def explore_tree(node1: TreeNode, node2: TreeNode, merged_node: TreeNode) -> None:
            merged_node.val = (node1.val if node1 is not None else 0) + (node2.val if node2 is not None else 0)
            left1 = node1.left if node1 is not None else None
            left2 = node2.left if node2 is not None else None
            if left1 is not None or left2 is not None:
                merged_node.left = TreeNode()
                explore_tree(left1, left2, merged_node.left)
            right1 = node1.right if node1 is not None else None
            right2 = node2.right if node2 is not None else None
            if right1 is not None or right2 is not None:
                merged_node.right = TreeNode()
                explore_tree(right1, right2, merged_node.right)
            
            return 
        
        explore_tree(root1, root2, merged_root)
        return merged_root
```

**幅優先(再帰)**

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1
        
        merged_root = TreeNode()
        def explore_tree(frontier: List[Tuple[TreeNode, TreeNode, TreeNode]]) -> None:
            if not frontier:
                return 

            next_frontier = []
            for node1, node2, merged_node in frontier:
                merged_node.val = (node1.val if node1 is not None else 0) + (node2.val if node2 is not None else 0)
                left1 = node1.left if node1 is not None else None
                left2 = node2.left if node2 is not None else None
                if left1 is not None or left2 is not None:
                    merged_node.left = TreeNode()
                    next_frontier.append((left1, left2, merged_node.left))
                right1 = node1.right if node1 is not None else None
                right2 = node2.right if node2 is not None else None
                if right1 is not None or right2 is not None:
                    merged_node.right = TreeNode()
                    next_frontier.append((right1, right2, merged_node.right))
            return explore_tree(next_frontier)

        explore_tree([(root1, root2, merged_root)])
        return merged_root
        
```

**入力を破壊する(幅優先)**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1
        
        merged_root = root1
        frontier = [(merged_root, root2)]
        while frontier:
            next_frontier = []
            for merged_node, node in frontier:
                merged_node.val += (node.val if node is not None else 0)

                left = node.left if node is not None else None
                if merged_node.left is None:
                    merged_node.left = left
                else:
                    next_frontier.append((merged_node.left, left))

                right = node.right if node is not None else None
                if merged_node.right is None:
                    merged_node.right = right
                else:
                    next_frontier.append((merged_node.right, right))
            frontier = next_frontier

        return merged_root
```
- merged_nodeとnodeという名前がややこしいかもしれない。

- 変換は、すべて5分くらい。
- 自由に変更できるようになってきた（コードをシンプルにできる余地はありそう）。




## 他の人のコードを見る。

1) https://github.com/rimokem/arai60/pull/23/changes#r3131122399
- 深さ優先、再帰、入力を破壊によるシンプルバージョン
- すごく見やすい。
- 自分のコードは、最初のコードに引っ張られて書いていて、とても長く感じる。
- 別のアプローチを考えるときは、最初からフラットに考えたほうがいいかもしれない。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right


    def mergeTrees(self, root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:
        if root1 is None:
            return root2
        if root2 is None:
            return root1
        
        root1.val += root2.val
        root1.left = self.mergeTrees(root1.left, root2.left)
        root1.right = self.mergeTrees(root1.right, root2.right)

        return root1 
```

2) https://github.com/Hiroto-Iizuka/coding_practice/pull/23/changes#r3137428484 のstep1
- まず、nodeの値を集め、合計値を求めながら、木を構築していく


3) https://github.com/dorxyxki/arai60/pull/23/changes のstep1
- 探索中、nodeが片方だけになったとき、それより深いnodeを非破壊でくっつける
- 上記のPRではdeepcopyを使っているが、なんでこんなに簡単に書けるのか、疑問に思ってCPythonを見に行った。 
  - https://github.com/python/cpython/blob/main/Lib/copy.py
  - が、全然読めない。すべての型に対応したり、データ構造に対応しようとして、遅くなっていそう。
  - みていてもわからないので、一旦おあずけ。deepcopyは避けて、自分でコピーするコードを書く。
- 再帰を使って、非破壊で書くなら以下の感じ。

```py
class Solution:
    def clone(self, node):
        if node is None:
            return None
        new_node = TreeNode(node.val)
        new_node.left = self.clone(node.left)
        new_node.right = self.clone(node.right)
        return new_node

    def mergeTrees(self, node1: Optional[TreeNode], node2: Optional[TreeNode]) -> Optional[TreeNode]:
        if node1 is None:
            return self.clone(node2)
        if node2 is None:
            return self.clone(node1)
        
        merged_node = TreeNode(node1.val + node2.val)
        merged_node.left = self.mergeTrees(node1.left, node2.left)
        merged_node.right = self.mergeTrees(node1.right, node2.right)

        return merged_node
```


- 全パターンでエラーを吐かずに3回書く。
