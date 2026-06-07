# 問題文
- https://leetcode.com/problems/search-insert-position/description/
- Given a sorted array of distinct integers and a target value, return the index if the target is found. If not, return the index where it would be if it were inserted in order.
- You must write an algorithm with O(log n) runtime complexity.

- Example 1:
- Input: nums = [1,3,5,6], target = 5
- Output: 2

- Example 2:
- Input: nums = [1,3,5,6], target = 2
- Output: 1

- Example 3:
- Input: nums = [1,3,5,6], target = 7
- Output: 4
 

- Constraints:
- 1 <= nums.length <= 104
- -10^4 <= nums[i] <= 10^4
- nums contains distinct values sorted in ascending order.
- -10^4 <= target <= 10^4

- アプローチ
  - （[アプローチの説明は整理してもう一度書き直しました](#アプローチ閉区間1)）
  - left と right を用いて、target が挿入される可能性のある範囲を管理する。
  - 各ループでまず次の2つを確認する。
  - nums[left] > target の場合、target は left の位置に挿入するのが適切なので left を返す。
  - nums[right] < target の場合、target は right の右側に挿入するのが適切なので right + 1 を返す。

  - 上記のどちらにも当てはまらない場合、(nums[left] <= target <= nums[right]が成り立つとき)、target の挿入位置は区間 [left, right] の中に存在するので、あたりをつける。
    - middle = (left + right) //2 を計算し、 nums[middle] を調べる。
    - nums[middle] == target の場合は middle を返す。
    - nums[middle] < target の場合、middle 以下の要素は挿入位置になり得ないため、探索範囲を [middle + 1, right] に更新する。
    - nums[middle] > target の場合、middle 以上の要素は挿入位置になり得ないため、探索範囲を [left, middle - 1] に更新する。
  
  - この操作を繰り返すことで、挿入位置を含む区間を徐々に狭めていく。


- **実行時間の見積もり**
- 探索範囲を半分ずつ狭めていくため、あたりを付ける動作は高々 O(log(len(nums))) 回である。
- 制約より len(nums) <= 10^4 なので、log2(10^4) ≒ 13.3 となり、ループ回数は高々 13〜14 回程度である。
- 各ループで行う処理は、比較や簡単な四則演算、添字アクセスなどの定数時間の処理のみである。
- 1 ループあたり数十ステップ程度と仮定すると、総ステップ数は 10³ ステップにも満たない。
- Python の実行速度を 10^7 ステップ/秒と仮定すると、10^3 ÷ 10^7 = 10^-4 秒程度であり、100 μs（0.1 ms）未満で処理が完了すると見積もられる。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while True:
            if nums[left] > target:
                return left
            if nums[right] < target:
                return right + 1
            
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle
            elif nums[middle] < target:
                left = middle + 1
            else:
                right = middle - 1

```

- `while True`が嫌がられるかもしれない。
- 探索範囲を更新していることがわかるような条件式にするといいかもしれないのと思い、修正した。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while nums[left] <= target <= nums[right]:            
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle
            elif nums[middle] < target:
                left = middle + 1
            else:
                right = middle - 1

        return left if nums[left] > target else right + 1
```

# 他の人のコードをみる
- コードをざっと見て、二分探索はコードを追うのが大変だという状況であることが分かった。
  - https://github.com/atmaxstar/coding_practice/pull/5
  - https://github.com/Manato110/LeetCode-arai60/pull/42
  - https://github.com/MasukagamiHinata/Arai60/pull/15#discussion_r3070735213
  - https://github.com/tom4649/Coding/pull/39/changes#diff-a454e5926956255042ab72f13c068ff340426126a0c235e5763f8db257b7768bR88-R111
  - https://discord.com/channels/1084280443945353267/1196498607977799853/1269532028819476562

- そこで、二分探索のコードをレビューしてもらうときに必要だと思った情報を自分でも考えてみた
- 必要なのは、区間の取り方とその区間が何を意味しているのか
  - 区間の取り方は開区間、閉区間、左半開区間、右半開区間の4つ
  - 区間の意味は問題次第。これをしっかり定義すれば、区間の更新についても説明がクリアになるだろう。

- とりあえず今回は、
  - 閉区間 or 右半開区間というパターン
  - 区間の意味を「targetがあるとすればこの中にある」 or 「targetの"挿入位置"があるとすればこの中になる」パターン
- に分けて考える。(計4パターン)


- まずは、自分で書いたコードの説明を修正する。

# アプローチ(閉区間1)
- 閉区間で探索を行う。閉区間は「targetがあるとすればこの中になる」という区間を指している。したがって初期値は[0, (numsの長さ) - 1]となる。
  - 以降ではleft = 0, right = (numsの長さ) - 1として説明する。
- 二分探索をしながら区間を縮小していく。
  - 区間の真ん中の値 nums[middle] を取り出す (middle = (left + right) // 2)。取り出した値に対し、
    - 1) nums[middle] == target ならば middle をreturnする。
    - 2) nums[middle] < targetなら、探索区間を[middle + 1, right]にする。
    - 3) target < nums[middle]なら、探索区間を[left, middle - 1]にする。
- 区間を縮小した結果、numsの中にtargetが見つからなかった場合を考える。（この場合returnするのは、targetの挿入位置になることに注意)
  - 見つからない状態を、left = middle = right で nums[middle] != targetとする。
  - nums[middle] < target ならば、middle + 1を返し、そうでなければ、middle を返せばよい。

- 上記の説明通りにもう一度コードを書いてみる。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums) - 1
        while left <= right:
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle

            if nums[middle] < target:
                left = middle + 1
            else:
                right = middle - 1 
        
        if nums[middle] < target:
            return middle + 1
        else:
            return middle
```

- 前回から条件式の書き方は変わったが、上記のような感じになる。

# アプローチ(閉区間2)
- 閉区間を「targetの"挿入位置"があるとすればこの中になる」として解くやり方。

- 初期値は [0, numsの長さ] とする。
- 区間 [left, right] は「挿入位置の候補」を表す。
- middle = (left + right) // 2 を取る。
- middle == numsの長さ の場合は、配列の末尾への挿入を意味する。
- それ以外では nums[middle] を参照し、
  - nums[middle] < target なら挿入位置は middle + 1 以降なので [middle + 1, right]
  - target <= nums[middle] なら挿入位置は middle 以前なので [left, middle]
  - 最後に left == right となり、その位置が挿入位置になる。したがって、leftかrightのどちらかを返す。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)

        while left < right:
            middle = (left + right) // 2

            if middle == len(nums):
                right = middle
            elif nums[middle] < target:
                left = middle + 1
            else:
                right = middle

        return left
```


# アプローチ(右半開区間1)

- 右半開区間で探索を行う。右半開区間は「targetがあるとすればこの中になる」という区間を指している。したがって初期値は [0, numsの長さ) となる。
  - 以降では left = 0, right = numsの長さ として説明する。
- 二分探索をしながら区間を縮小していく。
  - 区間の真ん中の値 nums[middle] を取り出す (middle = (left + right) // 2)。取り出した値に対し、
    - 1) nums[middle] == target ならば middle をreturnする。
    - 2) nums[middle] < target なら、探索区間を [middle + 1, right) にする。
    - 3) target < nums[middle] なら、探索区間を [left, middle) にする。
- 区間を縮小した結果、numsの中にtargetが見つからなかった場合を考える。（この場合returnするのは、targetの挿入位置になることに注意)
  - 見つからない状態を、left = right で nums[middle] != targetとする。
  - nums[middle] < target ならば、middle + 1を返し、そうでなければ、middle を返せばよい。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left = 0
        right = len(nums)

        while left < right:
            middle = (left + right) // 2

            if nums[middle] < target:
                left = middle + 1
            else:
                right = middle
                
        if nums[middle] < target:
            return middle + 1
        else:
            return middle
```



# アプローチ(右半開区間2)
- 右半開区間の意味を「targetの"挿入位置"があるとすればこの中になる」として解くやり方。
- 初期値は [0, numsの長さ) とする。以降では left = 0, right = numsの長さ として説明する。
- 二分探索をしながら区間を縮小していく。
  - 区間の真ん中の値 nums[middle] を取り出す (middle = (left + right) // 2)。取り出した値に対し、
    - 1) nums[middle] == target ならば、(ある意味ではmiddleに挿入するので、) middleをreturnする。
    - 2) nums[middle] < target なら、middle + 1より左の区間に挿入位置はないので、探索区間を [middle + 1, right) にする。
    - 3) target < nums[middle] なら、middleより右の区間に挿入位置はないので、探索区間を [left, middle) にする。
  - この操作により、常に「target の挿入位置が存在するとすれば探索区間の中にある」という性質を維持する。
- 区間を縮小した結果、最後は left = right になる。
  - このとき探索区間は [left, left) や [right, right)になっている。これが何を意味するのかについて、適切な言い回しが思いつかないが、leftかrightのどちらかを返せばよい。

```py
class Solution:
    def searchInsert(self, nums: List[int], target: int) -> int:
        left, right = 0, len(nums)
        while left < right:
            middle = (left + right) // 2
            if nums[middle] == target:
                return middle

            if nums[middle] < target:
                left = middle + 1
            else:
                right = middle
        return left
```

```py
            if nums[middle] == target:
                return middle
```
- がなくても動くが、あったほうが良いと思った。
