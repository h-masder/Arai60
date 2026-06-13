# 問題文
- https://leetcode.com/problems/search-in-rotated-sorted-array/description/

- There is an integer array nums sorted in ascending order (with distinct values).
- Prior to being passed to your function, nums is possibly left rotated at an unknown index k (1 <= k < nums.length) such that the resulting array is [nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]] (0-indexed). 
- For example, [0,1,2,4,5,6,7] might be left rotated by 3 indices and become [4,5,6,7,0,1,2].
- Given the array nums after the possible rotation and an integer target, return the index of target if it is in nums, or -1 if it is not in nums.
- You must write an algorithm with O(log n) runtime complexity.

- Example 1:
- Input: nums = [4,5,6,7,0,1,2], target = 0
- Output: 4

- Example 2:
- Input: nums = [4,5,6,7,0,1,2], target = 3
- Output: -1

- Example 3:
- Input: nums = [1], target = 0
- Output: -1


- Constraints:
- 1 <= nums.length <= 5000
- -10^4 <= nums[i] <= 10^4
- All values of nums are unique.
- nums is an ascending array that is possibly rotated.
- -10^4 <= target <= 10^4


# アプローチ
- [0, len(nums) - 1]の範囲のどこにあるのかを調べる。0をleft, len(nums) - 1をrightとする。
- 基本方針としては、二分探索を行うこと。境界がある場合は二分探索できないので、二分探索ができるようにリストを分割する。
  - 以下のようなイメージ
    - [4,5,6,7,0,1,2]を[4, 5, 6], [7], [0], [1, 2]に分割して、各分割リストに対して二分探索すればtargetがあるかどうかを判定できる
  - 分割の方法（および二分探索の方法）
    - リストの前半[left, middle]と後半[middle + 1, right]に分割 (middle = (left + right) // 2)
    - 分割した各リストは、境界があるかないか、の二パターン
    - 境界がある場合は、その配列に対して二分探索をする。切れ目があった場合は、さらに分割をする

# なぜこれでよいか
- 

- **実行時間の見積もり**
  - nums.length <= 5000より、高々13回でtargetが存在するかどうかが分かる。
  - リストを前半、後半に分けたり、二分探索する処理は、比較や加減算、除算くらいの簡単な処理であるため、それを数十ステップとすると、総ステップ数は10^2~10^3程度。
  - Pythonの実行速度を10^7ステップ/秒とすると、実行時間は10μs~100μs程度


```py
class Solution:
    def search(self, nums: List[int], target: int) -> int:
        NOT_FOUND = -1
        left = 0
        right = len(nums) - 1
        not_explored = [(left, right)]
        
        def binary_search(left, right, target):
            while left <= right:
                middle = (left + right) // 2
                if nums[middle] == target:
                    return middle
                
                if nums[middle] < target:
                    left = middle + 1
                else:
                    right = middle - 1
            
            return NOT_FOUND
        
        while not_explored:
            left, right = not_explored.pop()
            if nums[left] <= target <= nums[right]:
                return binary_search(left, right, target)
            if nums[left] > nums[right]:
                middle = (left + right) // 2
                not_explored.append((left, middle))
                not_explored.append((middle + 1, right))

        return NOT_FOUND
        
```

# 他の人のコードをみる。
- https://github.com/Manato110/LeetCode-arai60/pull/44
  - [0, len(nums) - 1]のどこにあるのかを調べる。0をleft, len(nums) - 1をrightとする。
  - O(log n) runtime complexityで解くために、リストの前半[left, middle]と後半[middle + 1, right]に分割しながら探す
    - targetがあるとすれば、リストの前半[left, middle]と後半[middle + 1, right]のどちらか、を判定する。
      - 判定方法：少なくとも前半と後半のいずれかは、昇順になっている（切れ目がない）。その区間の左端以上、かつ、右端以下であればその区間にある（targetがあるのなら）。そうでなければ、もう一方の区間にある。
  - 条件分岐がきれいで好み。こういう二分探索もあるなーと勉強になった。

- https://github.com/kitano-kazuki/leetcode/pull/43
  - Rotated array を sorted arrayとして扱うためのoffsetを使って探索をする。
    - 前問（https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/）のアプローチで、offsetを求めることができる。
  -  insertion_indexを求めている。素直にターゲットがあるかないかを判定するといいのでは、と感じた。
  - 境界を求めてそこを基準に分割して二分探索という考えを持つという考え方。
    - https://github.com/Yuto729/leetcode/pull/48

- https://github.com/mamo3gr/arai60/pull/41
 - bisectを使った方法
  - https://docs.python.org/3/library/bisect.html#bisect.bisect_left
  - bisect.bisect_left(a, x, lo=0, hi=len(a), *, key=None): Locate the insertion point for x in a to maintain sorted order. 
    - ということで、a = [1, 3, 5, 7] x = 4 なら 2が返る
 
  - `min_index = bisect.bisect_left(nums, True, key=lambda x: x <= nums[-1])`: で境界boundaryを探し、[0, boundary - 1]と[boundary, len(nums) - 1]に対して、bisec_leftを行う。挿入されたであろう位置のindexをみって一致しているか確認する

```py
class Solution:
    def search(self, nums: list[int], target: int) -> int:
        min_index = bisect.bisect_left(nums, True, key=lambda x: x <= nums[-1])
        # search in nums[:min_index]
        index = bisect.bisect_left(nums, target, lo=0, hi=min_index)
        if index < min_index and nums[index] == target:
            return index
        # search in nums[min_index:]
        index = bisect.bisect_left(nums, target, lo=min_index)
        if index < len(nums) and nums[index] == target:
            return index

        return -1
```

- うーん。これを使う気持ちはなんだろう。
- このライブラリは、ソート済みリストに対してソート順を維持したまま要素を挿入することを主な目的としているように見える。こういった使い方とは相性が悪く感じる。
- 生成AIに聞いてもピンとくる回答は得られず。一旦こういうものがあることだけ頭にいれて先に進む。
