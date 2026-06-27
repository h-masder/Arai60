# 問題文
- https://leetcode.com/problems/permutations/description/
- Given an array nums of distinct integers, return all the possible permutations. You can return the answer in any order.

- Example 1:
- Input: nums = [1,2,3]
- Output: [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

- Example 2:
- Input: nums = [0,1]
- Output: [[0,1],[1,0]]

- Example 3:
- Input: nums = [1]
- Output: [[1]]
 
- Constraints:
- 1 <= nums.length <= 6
- -10 <= nums[i] <= 10
- All the integers of nums are unique.


# アプローチ



- 
- 以下のような木を考えて、順列をつくる。

```text
                                  []
                    ┌─────────────┼────────────┐
                    │             │            │
                  [1]            [2]          [3]
                ┌──┴──┐        ┌──┴──┐      ┌──┴──┐
                │     │        │     │      │     │
             [1,2]    [1,3]  [2,1] [2,3]   [3,1] [3,2]
               │        │      │      │      │      │
               │        │      │      │      │      │
          [1,2,3] [1,3,2] [2,1,3] [2,3,1] [3,1,2] [3,2,1]
```

- 葉ノードのリストにまとめてreturnすればよい。



**実行時間の見積もり**
- n を `nums` の長さとする。
- 木の深さが増えるにつれて分岐数は `n`, `n-1`, `n-2`, ... と減っていくので、葉ノードは `n!` 個あり、 全ノード数は `1 + n + n(n-1) + n(n-1)(n-2) + ... `個であり、`O(n!)` 個である。
  - n <= 6なので、高々1+6+30+120+360+720+720=1957個
- 各ノードでは `nums` を一通り走査するので `n` 回程度処理する。さらにリストのコピーを行うので、全体で 1 ノード当たり `Θ(n^2)` 程度かかる。
- よって実行時間は `Θ(n^2 · n!)`。
- `n <= 6` なので、およそ`1957 × 6^2 = 70452` ステップ程度。
- Python の実行速度を `10^7` ステップ/秒とすると、実行時間は約 **7 ms** 程度。

```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        partial_permutations = [[]]
        while partial_permutations:
            partial_permutation = partial_permutations.pop()
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation)
                continue
            
            for i, num in enumerate(nums):
                if num in partial_permutation:
                    continue
                new_partial_permutation = partial_permutation + [num]
                partial_permutations.append(new_partial_permutation)

        return permutations
```

- 再帰でかも書いておく。
```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        def extend(partial_permutation):
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation)
                return

            for i, num in enumerate(nums):
                if num in partial_permutation:
                    continue
                new_partial_permutation = partial_permutation + [num]
                extend(new_partial_permutation)
            
            return
            
        extend([])
        return permutations
```

- backtrackingを調べた。共有している情報を書き換えるのに使うイメージ。
- partial_permutationを全体の情報として持ちたいときに、backtrackingを使うとうまく表現できる。

```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        def extend(partial_permutation):
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation.copy())
                return

            for i, num in enumerate(nums):
                if num in partial_permutation:
                    continue
                partial_permutation.append(num)
                extend(partial_permutation)
                partial_permutation.pop()
                
            return

        extend([])

        return permutations

```

- これをwhileで書くと、少し大変。` for i, num in enumerate(nums):`のあたりの情報を持つ必要がある。
  - indices で i を保持する。
```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []

        partial_permutation = []
        indices = [0]

        while indices:
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation.copy())

                partial_permutation.pop()
                indices.pop()
                if indices:
                    indices[-1] += 1
                continue

            i = indices[-1]
            while i < len(nums) and nums[i] in partial_permutation:
                i += 1

            if i < len(nums):
                indices[-1] = i
                partial_permutation.append(nums[i])
                indices.append(0)
            else:
                indices.pop()
                if partial_permutation:
                    partial_permutation.pop()
                if indices:
                    indices[-1] += 1

        return permutations
```


# 他の人のコードを見る。
- こちらは、見ながらコメントしていきます。
