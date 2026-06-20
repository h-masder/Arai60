# 問題文
- 

G- iven a binary search tree (BST) with a root node root and a target value v, the tree is partitioned into two subtrees, one of which has nodes that are both less than or equal to the target value and the other has nodes that are both greater than the target value, where the nodes of the given binary search tree root do not necessarily have nodes with values equal to v.

- In addition, most of the structure of the original tree root should be preserved. 
- Simply put, for any child node C that has a parent node P in the original tree, if they are both in the same subtree after the split, then the node C should still be a child node of P.
- For the two split subtrees, the one with the highest number of nodes is returned, or if the two subtrees have the same number of nodes, the one with the largest root node value is returned.

Example1:
Input:
root = {4,2,6,1,3,5,7}
v = 2
Output:
{4,3,6,#,#,5,7}
Explanation:
The given tree {4,2,6,1,3,5,7} is represented as the following:

          4
        /   \
       2     6
      / \   / \
     1   3 5   7

The two subtrees after splitting are:

          4
        /   \
      3      6      and    2
            / \           /
           5   7         1

The subtree with 4 as the root node has more nodes, so it returns the left subtree.

Example2:
Input:
root = {5,2,7,1,3,6}
v = 4
Output:
{5,#,7,6}
Explanation:
The given tree {5,2,7,1,3,6} is represented as the following:

         5
       /   \
      2     7
     / \   / 
    1   3 6   

The two subtrees after splitting are:

         2                  5
       /   \                 \
      1     3     and         7
                             /
                            6

Both subtrees have the same number of nodes, but the subtree with 5 as the root node has a larger value, so the right subtree is returned.


- constraint:
- The size of the BST will not exceed 50
- The BST is always valid and each node's value is different

- アプローチ
- 再帰によるアプローチを考えていたが、うまく分解できなかった。
- 生成AIと相談しながら、再帰によるアプローチに分解した。
- (入力を書き換えない方法や、splitする処理と同時にnode数をcountする方法を考えていたため、ワーキングメモリ不足に陥ったことに気がついた。一つずつ考えることが必要だった。)


- 分割
  - 各ノードは、自分の子ノードに対して、「子を根とする部分木を v以下の値で構成された木と vより大きい値で構成された木に分割して返す」よう依頼する。
  - 自分の子ノードが存在せず、空木 (None) に到達した場合は、2 本の空木 (None, None) を返す。
  - 子ノードは以下のように木を分割する。
    - node.val <= v の場合、右部分木の分割を子ノードに依頼する。（二分探索木の性質より、左部分木は v 以下の値で構成された木であることがすでにわかる。）
    - node.val > v の場合、左部分木の分割を子ノードに依頼する。（二分探索木の性質より、右部分木は v より大きい値で構成された木であることがすでにわかる。）
  - 子ノードから受け取った分割結果を用いて、自分がどちらの木に属するかを決定する。
    - node.val <= v の場合、v 以下の値で構成された木に属する。
    - node.val > v の場合、v より大きい値で構成された木に属する。
  - 自分が属する側の木に、子ノードから受け取った対応する部分木を接続する。

- node数のカウント
  - それぞれの木についてノード数を再帰的に数える。
  - 後は問題文のとおりに返す。



**実行時間の見積もり**
- The size of the BST will not exceed 50であり、分割とnode数のカウントでそれぞれ50回のメモリアクセス。
- 各処理では、比較や加算などの簡単な処理がコード数行から数十行程度で終わるためそれを数十ステップとすると、総ステップ数は10^3くらい。
- Pythonの実行速度を10^7ステップ/秒とすると、1msくらい。

```py
class Solution:
    def split_b_s_t(self, root: TreeNode, v: int) -> TreeNode:
        def split(node):
            if node is None:
                return None, None

            if node.val <= v:
                smaller, larger = split(node.right)
                node.right = smaller
                return node, larger
            else:
                smaller, larger = split(node.left)
                node.left = larger
                return smaller, node
        
        def count(node):
            if node is None:
                return 0
            return 1 + count(node.left) + count(node.right)

        smaller, larger = split(root)

        if count(smaller) <= count(larger):
            return larger
        return smaller
```

- 入力を書き換えないようにするには、最初に木を丸まるコピーしてからそれに対して実行すればよい。

- 一応whileにも変換しておく。



```py
class Solution:
    def split_b_s_t(self, root: TreeNode, v: int) -> TreeNode:
        def split(node):
            smaller_dummy = TreeNode(0)
            larger_dummy = TreeNode(0)

            smaller_node = smaller_dummy
            larger_node = larger_dummy
            
            while node:
                if node.val <= v:
                    next_node = node.right

                    node.right = None
                    smaller_node.right = node

                    smaller_node = smaller_node.right
                    node = next_node
                else:
                    next_node = node.left

                    node.left = None
                    larger_node.left = node

                    larger_node = larger_node.left
                    node = next_node
                
            return smaller_dummy.right, larger_dummy.left

        def count(node):
            count = 0
            not_visited_nodes = [node]
            while not_visited_nodes:
                node = not_visited_nodes.pop()
                if node is not None:
                    count += 1
                    not_visited_nodes.extend([node.left, node.right])

            return count

        smaller, larger = split(root)
        if count(smaller) <= count(larger):
            return larger
        return smaller
```


# 他の人のコードを見る

- https://github.com/h1rosaka/arai60/pull/62 のSTEP2のループ
  - 元の再帰を変換するなら、こんな感じだと思うが読みにくい。
  - コメントなどに対応して、コードを修正した
    - https://github.com/h1rosaka/arai60/pull/62/changes#r3288760519 


```py
class Solution:
    def split_b_s_t(self, root: TreeNode, v: int) -> TreeNode:
        def split(root):
            def connect(parent, side, child):
                if side == "left":
                    parent.left = child
                else:
                    parent.right = child

            dummy_low = TreeNode(0)
            dummy_high = TreeNode(0)

            nodes = [(root, dummy_low, "left", dummy_high, "right")]

            while nodes:
                node, parent_low, side_low, parent_high, side_high = nodes.pop()

                if node is None:
                    connect(parent_low, side_low, None)
                    connect(parent_high, side_high, None)
                    continue

                if node.val <= v:
                    connect(parent_low, side_low, node)
                    nodes.append((node.right, node, "right", parent_high, side_high))
                else:
                    connect(parent_high, side_high, node)
                    nodes.append((node.left, parent_low, side_low, node, "left"))

            return dummy_low.left, dummy_high.right
        
        def count(node):
            not_visited_node = [node]
            count = 0
            
            while not_visited_node:
                node = not_visited_node.pop()
                if node is not None:
                    count += 1
                    not_visited_node.extend([node.left, node.right])
            return count

        smaller, larger = split(root)

        if count(smaller) <= count(larger):
            return larger
        return smaller
```

- splitの部分をすらすら書くことは大変。
- 再帰のほうが圧倒的に読みやすいパターンもあることが分かった。
