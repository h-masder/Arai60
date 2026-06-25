# 問題文
- https://leetcode.com/problems/subsets/

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
- 方針は46. Permutationsと似たもの
```text
                                [1, 2, 3]
                  /                |                \
               [1, 2]            [2, 3]           [1, 3]
              /     \           /     \          /     \
          [1]       [2]      [2]      [3]      [1]    [3]

```

- numsを根として、、分割しながらsubsetを構成する。
- 幅優先探索、深さ優先探索、どちらでもいいし、再帰とループどちらでもいいが、深さ優先の再帰で書く。

- 再帰
  - 葉：permutationがnumsと同じ長さなので、返り値のリストにappendする。
  - その他：親から作りかけのpermutation(pertial_permutation)を受け取る。numsの各要素を見て、pertial_permutationの中にそれがなければ、追加して子に渡す。
  - 46.Permutationsと比較して、気をつけることは重複を許さないこと。
  - setで訪れた重複を管理し、一度訪れたらそれ以降はやらない。setにはsubsetsをsortedしてtupleしたものを入れる。
  - 

**実行時間の見積もり**
- 関数が呼び出される回数は、subsetsの個数である2^n程度（nはnums.lengthで、nums.length <= 10）なので、高々1024程度
- 各関数呼び出しごとにsubsetsに対するsortedが走るので、O(nlogn)くらいかかる。つまり、30ちょっとのステップ数
- 余裕をもって見積もってもそうステップ数は10^4くらいPythonの実行速度を10^7ステップ/秒とすると、1msくらい。

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = [[]]
        visited = set()
        def divide(current_subset):
            all_subsets.append(current_subset)
            
            for i in range(len(current_subset)):
                next_subset = current_subset[:i] + current_subset[i + 1:]
                if not next_subset:
                    continue
                sorted_subset = tuple(sorted(next_subset))
                if sorted_subset in visited:
                    continue
                
                visited.add(sorted_subset)
                divide(next_subset)
            
        divide(nums)
        return all_subsets
```

- ループ
```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = [[]]
        visited = set()
        current_subsets = [nums]
        while current_subsets:
            current_subset = current_subsets.pop()
            all_subsets.append(current_subset)
            for i in range(len(current_subset)):
                next_subset = current_subset[:i] + current_subset[i + 1:]
                if not next_subset:
                    continue
                sorted_subset = tuple(sorted(next_subset))
                if sorted_subset in visited:
                    continue
            
                visited.add(sorted_subset)
                current_subsets.append(next_subset)
            
        return all_subsets
```

- backtrackingでやるなら、46.Permutationsのようにrootは[]にして伸ばす。
```text
                []
        ┌────────┼────────┐
       [1]      [2]      [3]
      /   \       \        
   [1,2] [1,3]   [2,3]
     |
 [1,2,3]
```
- 各ノードをappendする。

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        def extend(start, current_subset):
            all_subsets.append(current_subset.copy())
            
            for i in range(start, len(nums)):
                current_subset.append(nums[i])
                extend(i + 1, current_subset)
                current_subset.pop()

            return
            
        extend(0, [])
        return all_subsets
```

# 他の人のコードを見てコメントを残す。
- numsの各要素で「入れる/入れない」の2択
  - https://github.com/Yuto729/leetcode/pull/55

```text
                        []
               ┌─────────┴─────────┐
              []                  [1]
        ┌─────┴─────┐       ┌─────┴─────┐
       []         [2] 　   [1] 　      [1,2]
    ┌──┴──┐     ┌──┴──┐   ┌─┴─┐       ┌─┴─┐
   []   [3]   [2]   [2,3] [1] [1,3] [1,2] [1,2,3]
```
- このうち、葉のみall_subsetsにappendする。

```py
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        all_subsets = []
        index_and_subset = [(0, [])] 

        while index_and_subset:
            index, current_subset = index_and_subset.pop()
            if index == len(nums):
                all_subsets.append(current_subset) # 葉のみappend
                continue

            index_and_subset.append((index + 1, current_subset))
            index_and_subset.append((index + 1, current_subset + [nums[index]]))

        return all_subsets
```
