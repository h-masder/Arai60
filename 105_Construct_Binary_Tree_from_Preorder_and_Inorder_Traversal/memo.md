## 問題
https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/

Given two integer arrays preorder and inorder where preorder is the preorder traversal of a binary tree and inorder is the inorder traversal of the same tree, construct and return the binary tree.
Constraints:
1 <= preorder.length <= 3000
inorder.length == preorder.length
-3000 <= preorder[i], inorder[i] <= 3000
preorder and inorder consist of unique values.
Each value of inorder also appears in preorder.
preorder is guaranteed to be the preorder traversal of the tree.
inorder is guaranteed to be the inorder traversal of the tree.

## 進め方
- 最近いろいろなやり方を模索しています。かなり迷走していますが、ひとまずこれでやります。
  - (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
    - 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
  - (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
  - (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
    - レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
      - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
      - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。

## アプローチ

- 簡単な例をいくつか考えた（後で載せます）
- その結果、preorderのからrootを取り出す。inorderリストのうち、rootより左のリストの中身が左部分木、rootより右のリストの中身が右部分木になる。
- 上記の処理を続けることで、二分木ができる。
- rootの取り出し方は、ちょっと悩んだが、まずは必ずinorderを全部走査することにする。それができたら、高速化を考える。

**実行時間の見積もり**
- rootをpreorderの要素分だけ見つける。rootを見つけるとき、preorderを走査するので、全体は(3*10^3)*(3*10^3)くらいのメモリアクセス。
- Pythonの実行時間を10^7/秒とすると、だいたい数秒かかる。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        def find_inorder_root_index(inorder_left, inorder_right):
            for i in range(len(preorder)):
                for j in range(inorder_left, inorder_right):
                    if preorder[i] == inorder[j]:
                        return j

        def build_tree(inorder_left: int, inorder_right: int) -> Optional[TreeNode]:
            if inorder_right <= inorder_left:
                return None

            inorder_root_index = find_inorder_root_index(inorder_left, inorder_right)
            node = TreeNode(val=inorder[inorder_root_index])
            node.left = build_tree(inorder_left, inorder_root_index)  
            node.right = build_tree(inorder_root_index + 1, inorder_right)
            return node

        
        return build_tree(0, len(preorder))
```

- あとはこれのfind_inorder_root_indexの高速化を考える。
- find_root_indexでリストを走査する代わりに、HashMapを使う。
- 3*10^3くらいのメモリアクセスになり、Pythonの実行時間を10^7/秒とすると、だいたい数ミリ秒かかる。


```py
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        value_to_inorder_index = {value: i for i, value in enumerate(inorder)}
        def build_tree(inorder_left_index, inorder_right_index, preorder_root_index):
            if inorder_right_index <= inorder_left_index:
                return None, preorder_root_index
            
            preorder_root_value = preorder[preorder_root_index]
            node = TreeNode(val=preorder_root_value)
            preorder_root_index += 1

            inorder_root_index = value_to_inorder_index[preorder_root_value]
            node.left, preorder_root_index = build_tree(inorder_left_index, inorder_root_index, preorder_root_index)
            node.right, preorder_root_index = build_tree(inorder_root_index + 1, inorder_right_index, preorder_root_index)
            return node, preorder_root_index
            
        root, _ = build_tree(0, len(inorder), 0)
        return root
```

- 再帰で書いてみたがpreorder_indexを渡さないといけないので、見にくい。
- このタイプはwhileで書いて、preorder_root_indexを引数にしないとシンプルになる。
- もしくは、nonlocalのほうが分かりやすいかも。nonlocalはあんまり好みではないけど、練習する。

- whileで書く
```py
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        if not inorder:
            return None
        value_to_inorder_index = {value: i for i, value in enumerate(inorder)}

        root = TreeNode()
        node_and_inorder_ranges = [(root, 0, len(inorder))]
        preorder_root_index = 0
        while node_and_inorder_ranges:
            preorder_root_value = preorder[preorder_root_index]
            preorder_root_index += 1

            node, inorder_left_index, inorder_right_index = node_and_inorder_ranges.pop()
            node.val = preorder_root_value

            inorder_root_index = value_to_inorder_index[preorder_root_value]
            if inorder_root_index + 1 < inorder_right_index:
                node.right = TreeNode()
                node_and_inorder_ranges.append((node.right, inorder_root_index + 1, inorder_right_index))
            if inorder_left_index < inorder_root_index:
                node.left = TreeNode()
                node_and_inorder_ranges.append((node.left, inorder_left_index, inorder_root_index))

        return root

```

- nonlocalを使う
```py
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        value_to_inorder_index = {value: i for i, value in enumerate(inorder)}
        preorder_root_index = 0
        def build_tree(inorder_left_index, inorder_right_index):
            nonlocal preorder_root_index
            if inorder_right_index <= inorder_left_index:
                return None
            
            preorder_root_value = preorder[preorder_root_index]
            node = TreeNode(val=preorder_root_value)
            preorder_root_index += 1

            inorder_root_index = value_to_inorder_index[preorder_root_value]
            node.left = build_tree(inorder_left_index, inorder_root_index)
            node.right = build_tree(inorder_root_index + 1, inorder_right_index)
            return node
            
        return build_tree(0, len(inorder))
```


## 他の人の解答を見る。
- inorderでノードを走査しながら、preorderの順序を使って木を構築する
  - https://github.com/Yuto729/LeetCode_arai60/pull/34/changes#diff-c39c2922eecae24bac56f4e9948659d7e04a10c11bbf0abbb77fef1a831f52c6R189-R193 の inorder順に構築するスタックベース解法

  - 挙動を理解し、「これでいいかもしれない」と思えるまでに数日かかった。完全に正しいという確証は得られていないが、そこまで深入りする必要もないため、次に進むことにした。
    - ひとまずこういうやりかたもある、ということを知っておけばよい。こうしたコードを見たときに驚かなければ十分であり、必要に迫られたとき(こういうアルゴリズムで実装する必要があったり、こういうコードを修正するなど)には時間をかけて完全に理解し、説明できればよいだろう。
    - これまでの理解はinorder.pngに記載しています。

```py
class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:
        value_to_preorder_index = {value: i for i, value in enumerate(preorder)}

        descendants = []
        def build_right_subtree(ancestor):
            right_subtree_head = None

            while descendants:
                if value_to_preorder_index[descendants[-1].val] < value_to_preorder_index[ancestor.val]:
                    break
                node = descendants.pop()
                node.right = right_subtree_head
                right_subtree_head = node
            return right_subtree_head
        
        def build_right_subtree_of_root():
            root = None
            while descendants:
                node = descendants.pop()
                node.right = root
                root = node
            return root

        for value in inorder:
            node = TreeNode(val=value)
            node.left = build_right_subtree(node)
            descendants.append(node)

        return build_right_subtree_of_root()
```

- preorderでノードを走査しながら、inorderの順序を使って木を構築する
  - https://github.com/Yuto729/LeetCode_arai60/pull/34/changes#diff-c39c2922eecae24bac56f4e9948659d7e04a10c11bbf0abbb77fef1a831f52c6R189-R193 の アルゴリズム（inorder位置をスタックに持つ版）
  - こちらもひとまず挙動を理解したが、こういった解法もある程度でいいかな。


- 解法のエッセンス
  - https://discord.com/channels/1084280443945353267/1478763507963924522/1492871022511390843 からの会話


- 感想
  - この問題に対するいろいろな人の反応を見れてよかった。
