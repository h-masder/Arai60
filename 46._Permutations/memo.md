# 問題文

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
```text
                                   []
                  /                |                \
                [1]               [2]              [3]
              /     \           /     \          /     \
         [1,2]     [1,3]   [2,1]    [2,3]     [3,1]    [3,2]
           |          |       |         |       |         |
      [1,2,3]   [1,3,2]   [2,1,3]    [2,3,1] [3,1,2]  [3,2,1]
```

- 順列を作る。作り方は、上記の木のようなイメージで、根は[]で、場合分けしながら構成し、葉にになったらpermutationができている。
- 幅優先探索、深さ優先探索、どちらでもいいし、再帰とループどちらでもいいが、深さ優先の再帰で書く。

- 再帰
  - 葉：permutationがnumsと同じ長さなので、返り値のリストにappendする。
  - その他：親から作りかけのpermutation(pertial_permutation)を受け取る。numsの各要素を見て、pertial_permutationの中にそれがなければ、追加して子に渡す。

**実行時間の見積もり**
- 関数が呼び出される回数は、O(n!)くらい。6!で720くらい。
- 各関数では、numsの各要素を見る。これが6なので、トータルで10^4くらいのそうステップ数
- Pythonの実行速度を10^7ステップ/秒とすると、1msくらい。

```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        def extend(partial_permutation):
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation)
                return
            
            for num in nums:
                if num in partial_permutation:
                    continue
                extend(partial_permutation + [num])
        
        extend([])
        return permutations
```


- backtracking
- まずは、調べた。
- 自分の中の理解は、木構造の全ノードで共有したい情報に対して、適用するのが使い道だと思った。
- 先ほどの再帰は、親からデータをもらうだけで、子からは何も受け取っていないが、backtrackingを使って、同じ情報を共有できる。
```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        def extend(partial_permutation):
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation.copy())
                return
            
            for num in nums:
                if num in partial_permutation:
                    continue
                partial_permutation.append(num)
                extend(partial_permutation)
                partial_permutation.pop()
            
            return
        
        extend([])
        return permutations
```

- 一応、ループ
- 今回はbacktrackingを使う必要はないと感じた。
```py
class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        permutations = []
        partial_permutations_and_remaining_nums = [([], nums)]

        while partial_permutations_and_remaining_nums:
            partial_permutation, remaining_nums = partial_permutations_and_remaining_nums.pop()
            if len(partial_permutation) == len(nums):
                permutations.append(partial_permutation)

            for i, num in enumerate(remaining_nums):
                next_partial_permutation = partial_permutation + [num]
                next_remaining_nums = remaining_nums[:i] + remaining_nums[i + 1:]
                partial_permutations_and_remaining_nums.append((next_partial_permutation, next_remaining_nums))
        
        return permutations
```
- 若干名前が長い。

# 他の人のコードをみる
- 気づいたことはコメントする。
