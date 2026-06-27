# 問題文
- https://leetcode.com/problems/subsets/description/

- Given an integer array nums of unique elements, return all possible subsets (the power set).
- The solution set must not contain duplicate subsets. Return the solution in any order.

- Example 1:
- Input: nums = [1,2,3]
- Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]

- Example 2:
- Input: nums = [0]
- Output: [[],[0]]
 
- Constraints:

- 1 <= nums.length <= 10
- -10 <= nums[i] <= 10
- All the numbers of nums are unique.

# アプローチ
- 前問(46. Permutations)と考え方はほぼ同じ。

```text
                                              ([], 0)
                             ┌──────────────────┼──────────────────┐
                             │                  │                  │
                         ([1], 1)          ([2], 2)          ([3], 3)
                        ┌─────┴─────┐            │
                        │           │            │
                  ([1,2], 2)   ([1,3], 3)   ([2,3], 3)
                        │
                        │
                  ([1,2,3], 3)
```

- こんな木を作って、subsetsに入れていく。各ノードの左の値がsubsetの要素
- 各ノードの右の値は、子に向かってsubsetの構築を依頼するときに、numsをどこから見ればいいのかを伝えるための変数。


**実行時間の見積もり**
- `n` を `nums` の長さとする。
- 部分集合は全部で `2^n` 個なので、探索木の全ノード数も `2^n` 個である。
  - `n <= 10` より、高々 `2^10 = 1024` 個。
- 各ノードでは `current_subset + [nums[i]]` によるリストのコピーがあり、高々 `n` 要素をコピーする。
- よって総ステップ数は、高々 `1024 × 10 = 10240` ステップ程度。
- Python の実行速度を `10^7` ステップ/秒とすると、実行時間は約1 ms程度。

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        subset_and_indices = [([], 0)]
        while subset_and_indices:
            current_subset, index = subset_and_indices.pop()
            all_subsets.append(current_subset)
            for i in range(index, len(nums)):
                new_subset = current_subset + [nums[i]]
                subset_and_indices.append((new_subset, i + 1))
        
        return all_subsets
```

- 一応、再帰
```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        def extend(current_subset, index):
            all_subsets.append(current_subset)
            
            for i in range(index, len(nums)):
                new_subset = current_subset + [nums[i]]
                extend(new_subset, i + 1)
        extend([], 0)
        return all_subsets
```

- backtracking
```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        def extend(current_subset, index):
            all_subsets.append(current_subset.copy())
            
            for i in range(index, len(nums)):
                current_subset.append(nums[i])
                extend(current_subset, i + 1)
                current_subset.pop()
        extend([], 0)
        return all_subsets
```

# 他の人のコードを読み、気づいたことはコメントする。
- 取り合えず、次の問題(Combination sum)とその次の問題(Generate Parentheses)が同じような問題なので、やることは変わらなそうなので、それを解くことにする。
