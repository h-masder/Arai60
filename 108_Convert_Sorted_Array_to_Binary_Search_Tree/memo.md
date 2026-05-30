## 問題
https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/

Given an integer array nums where the elements are sorted in ascending order, convert it to a height-balanced binary search tree.
A height-balanced binary tree is a binary tree in which the depth of the two subtrees of every node never differs by more than one.

Constraints:
1 <= nums.length <= 104
-104 <= nums[i] <= 104
nums is sorted in a strictly increasing order.

## 進め方

- (step1) 自分で考える。面接を意識してどういったアプローチで書くのか記述する。書く前に時間計算量を見積もる。時間制限はEasyなら15分、mediumなら30分(アプローチや、実行時間を書くことも含む)。
  - https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
- (step2) 他の人のコードを見て(レビューして)、自分のコードと比較して修正する。さらに、見たコードに対してコメントを残す。レビューの仕方は以下を参考にする。
  - https://google.github.io/eng-practices/review/reviewer/looking-for.html
- (step3) エラーをはかずに3回書けるようにする。

## アプローチ
- 入力は List[int]、出力はTreeNode
- List[int]が空の場合は、Noneを返すことにする。
- 同じ深さの木を構築するのであれば、要素をはじめから見ていき、完全二分木を構築すればよい。
  - ここで, A height-balanced binary treeの定義の理解と、Exampleの例がなんとなく意図が違うと感じた。A height-balanced binary treeの定義を見た感じ、値の入れ方は適当でよさそうだが、Exampleをみるとそうではない。
  - 用語を正確にわかっていない気がしたので、wikipediaをみた。
    - a binary search tree (BST), also called an ordered or sorted binary tree, is a rooted binary tree data structure with the key of each internal node being greater than all the keys in the respective node's left subtree and less than the ones in its right subtree.(https://en.wikipedia.org/wiki/Binary_search_tree)
    - a binary tree is a tree data structure in which each node has at most two children, referred to as the left child and the right child. (https://en.wikipedia.org/wiki/Binary_tree)
    - height balancedであり、ordered なbinary treeを構築する問題であることを理解した。そもそもbinary treeとbinary search treeの区別もついていなかった。気を取り直して、height-balanced binary search treeを作る。
- 結果的に、うまく作れなかった。height-balanced treeの構築は以下のコードのようにすればいいかなと思ったが、ノードの値の入れ方がうまくかけない。numsの真ん中の値から入れていけばよいかなと思ったけど、この手の処理をイメージして書くのがかなり苦手。


**実行時間の見積もり**
- 配列(nums)の要素に一回ずつアクセスすれば木が構築できる(最大10^4回のメモリアクセス)
- Pythonの実行時間を10^7/秒とすると、数ミリ秒かかる。


**幅優先(未完成)**
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        
        root = TreeNode(val=nums[0])
        frontier = deque([root])
        i = 1
        while i < len(nums):
            node = frontier.popleft()

            node.left = TreeNode(val=nums[i])
            frontier.append(node.left)
            i += 1

            if i < len(nums):
                node.right = TreeNode(val=nums[i])
                frontier.append(node.right)
                i += 1
        
        return root
```

- 時間を延長して解こうとしたが、そもそも絵でかけない。何が足りていないのか他の人の解答見て確かめる。



- 見たコード: https://github.com/rimokem/arai60/pull/24
  - 深さ優先で解いている。深さ優先でheight-balancedを保てるのはなぜかわからないけど、それは後で考えるとする(結局こちらはすぐに解決した)。
  - 深さ優先を幅優先に変更して、コードを追ってみる。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None

        root = TreeNode()
        frontier = deque([(root, 0, len(nums) - 1)])
        while frontier:
            node, left, right = frontier.popleft()
            mid = (left + right) // 2
            node.val = nums[mid]

            if left < mid:
                node.left = TreeNode()
                frontier.append((node.left, left, mid - 1))
            if mid < right:
                node.right = TreeNode()
                frontier.append((node.right, mid + 1, right))
        return root
```

コードを追った結果、
- `frontier.append((node.left, left, mid - 1))`や`frontier.append((node.right, mid + 1, right))`が自分の絵と違っている部分だった。
- 自分は、`frontier.append((node.left, left, mid))`や`frontier.append((node.right, mid, right))`で考えていて、うまく書けなかった。
  - (自分向けのメモ: 真ん中の値を“その区間の根”にして、「残り」を左右の区間に分ける」)

- 考え方とコードの表現がリンクしたので、あとはいろいろと別の解きかたを書いてみる。
- まずは、幅優先で同じ深さのノードを一気に(同じforループのブロックで)構築する方法。
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        
        root = TreeNode()
        frontier = [(root, 0, len(nums) - 1)]
        while frontier:
            next_frontier = []
            for node, left, right in frontier:
                mid = (left + right) // 2
                node.val = nums[mid]

                if left < mid:
                    node.left = TreeNode()
                    next_frontier.append((node.left, left, mid - 1))

                if mid < right:
                    node.right = TreeNode()
                    next_frontier.append((node.right, mid + 1, right))
            
            frontier = next_frontier
        return root
```
- 幅優先はこの表現方法が一番好きかもしれない。

- 上記のことを考えているうちに、深さ優先でも解ける理由はわかった。
- 探索する順番を変えても、木が偏って深くなったりしない。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        
        root = TreeNode()
        frontier = [(root, 0, len(nums) - 1)]
        while frontier:
            node, left, right = frontier.pop()

            mid = (left + right) // 2
            node.val = nums[mid]

            if left < mid:
                node.left = TreeNode()
                frontier.append((node.left, left, mid - 1))

            if mid < right:
                node.right = TreeNode()
                frontier.append((node.right, mid + 1, right))

        return root

```
- 
- 再帰なら、以下のような感じ。

```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None

        def generate_binary_search_tree(node: TreeNode, left: int, right: int) -> None:

            mid = (left + right) // 2
            node.val = nums[mid]

            if left < mid:
                node.left = TreeNode()
                generate_binary_search_tree(node.left, left, mid - 1)

            if mid < right:
                node.right = TreeNode()
                generate_binary_search_tree(node.right, mid + 1, right)

        root = TreeNode()
        generate_binary_search_tree(root, 0, len(nums) - 1)

        return root
```

## 他の人の解答をみる(見た解答にコメントも残す)

- 1)他の方の再帰をみてみた。
  - https://github.com/rimokem/arai60/pull/24
  - https://github.com/Manato110/LeetCode-arai60/pull/24
  - https://github.com/tom4649/Coding/pull/23
  - https://github.com/kitano-kazuki/leetcode/pull/24/changes#r2957795289
  - 考え方は同じだが、コード表現がいくつか違う。シンプルさを考えると、どれもシンプルで良い。

  - 基本的には考え方は似ている。
    -「部下に作成をお願いした木の根を左右の子に、中央値を値にしたノードを根として作成して返します。」

- (tom4649さんのコード)
```py
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def sortedArrayToBST(self, nums: List[int]) -> Optional[TreeNode]:
        if not nums:
            return None
        
        mid = len(nums) // 2

        return TreeNode(val=nums[mid], left=self.sortedArrayToBST(nums[:mid]), right=self.sortedArrayToBST(nums[mid+1:]))
```

2) frontierという変数名について
  - frontier は幅優先探索で未探索の最前線のノードの集合を表す際に使うように思います。深さ優先探索ではあまり使わない印象があります。
    - https://github.com/kitano-kazuki/leetcode/pull/24/changes#r2964278699
    - frontierも使われているという意見もある。自分の中では、深さ優先ならfrontierでないほうがいいかもしれないという気持ち


- 最後にここにある全パターンで3回連続でパスするまで書く。
  - はじめはぎこちなかったが、だいぶ慣れた。


## メモ
- 再帰のデメリットについて
  - https://github.com/Manato110/LeetCode-arai60/pull/24/changes#r3103093599

- 今回の問題は、だいぶ簡単な部類になると思うが、できなくてだいぶショック。
> 練習会などで、お互いに初見の問題を提示して解くとかをしているのですが、
> 「だいたい medium くらいの問題は、10分くらいでエラーのないコードがホワイトボードに書ける」くらいが見ていると達成されています。(エラーのない、は、もちろん100%とはいわないですが、とはいえ、ほぼ達成されています。解説をお願いすると、細かいミスがあってもその場で修正されます。)
- これにたどりつくのか？
