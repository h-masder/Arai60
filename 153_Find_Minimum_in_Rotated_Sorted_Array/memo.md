# 問題文
- https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/description/
- Suppose an array of length n sorted in ascending order is rotated between 1 and n times. For example, the array nums = [0,1,2,4,5,6,7] might become:

- [4,5,6,7,0,1,2] if it was rotated 4 times.
- [0,1,2,4,5,6,7] if it was rotated 7 times.
- Notice that rotating an array [a[0], a[1], a[2], ..., a[n-1]] 1 time results in the array [a[n-1], a[0], a[1], a[2], ..., a[n-2]].
- Given the sorted rotated array nums of unique elements, return the minimum element of this array.
 -You must write an algorithm that runs in O(log n) time.

- Example 1:
- Input: nums = [3,4,5,1,2]
- Output: 1
- Explanation: The original array was [1,2,3,4,5] rotated 3 times.

- Example 2:
- Input: nums = [4,5,6,7,0,1,2]
- Output: 0
- Explanation: The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

- Example 3:
- Input: nums = [11,13,15,17]
- Output: 11
- Explanation: The original array was [11,13,15,17] and it was rotated 4 times. 

- Constraints:
- n == nums.length
- 1 <= n <= 5000
- -5000 <= nums[i] <= 5000
- All the integers of nums are unique.
- nums is sorted and rotated between 1 and n times.

# アプローチ
- 空リストは考えないものとする。(もし仮に空リストに対処するなら、 `if not nums` で処理する)
- 「出力したい値 min_value は、常にこの中に含まれている」という閉区間を設定する。
   - 初期値は[0, len(nums) - 1]
   - 初期値の0をleft, len(nums) - 1をrightとする。
- ループを回しながら、この区間を狭めていく。最終的にはleft = rightとなった時点でループを抜ける。このとき、min_value = nums[left] = [right]なので、nums[left]かnums[right]を返せばよい。
- ループの回し方
  - middle = (left + right) // 2 を計算する。(このときleft <= middle < rightが成り立っている)
  - min_valueは[left, middle]か[middle + 1, right]に含まれることが分かる。どちらに含まれているか調べるためには以下の処理を行う
    - nums[middle] < nums[right]かどうか調べる。
      - もしそうなら、閉区間[left, middle]にmin_valueが存在するので、right = middleに更新する。
      - そうでないなら、閉区間[middle + 1, right]にmin_valueが存在するので、left = middle + 1に更新する。

**実行時間の見積もり**
- 長さが高々5000であるnumsを二分探索する。numsへのメモリアクセスは高々13回(5000 < 2^13より)
- メモリアクセス時の処理は、比較や足し算引き算だけであり、それを数十ステップ程度とみなすと、総ステップ数は10^2~10^3程度
- Pythonの実行速度を10^7ステップ/秒とすると、実行時間は10μs~100μsくらい。

```py
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while left < right:
            middle = (left + right) // 2
            if nums[middle] < nums[right]:
                right = middle
            else:
                left = middle + 1

        return nums[left]
```

- 視野を広げることを目的に別の方法を考えてみる。
-  区間設定は変えない。
   - 初期値は[0, len(nums) - 1]
   - 初期値の0をleft, len(nums) - 1をrightとする。
- ループを抜ける条件を変えてみる。「nums[left] > nums[right]でなければループを抜ける」という条件にする。
- ループを抜けるときは、nums[left] <= nums[right]であり、 nums[left]が min_valueとなる。
- ループの回し方
  - middle = left + (right - left) // 2 を計算する。(このときleft <= middle < rightが成り立っている)
  - min_valueは[left, middle]か[middle + 1, right]に含まれることが分かる。どちらに含まれているか調べるためには以下の処理を行う
    - nums[left] <= nums[middle]かどうか調べる。
      - もしそうなら、閉区間[middle + 1, right]にmin_valueが存在するので、left = middle + 1に更新する。
      - そうでないなら、閉区間[left, middle]にmin_valueが存在するので、right = middleに更新する。

```py
class Solution:
    def findMin(self, nums: List[int]) -> int:
        left = 0
        right = len(nums) - 1
        while nums[left] > nums[right]:
            middle = (left + right) // 2
            if nums[left] <= nums[middle]:
                left = middle + 1
            else:
                right = middle

        return nums[left]
```

# 他の人のコードを見る。

- https://github.com/kitano-kazuki/leetcode/pull/42 の Code1-2 (Binary Search)
- 解き方は、上の二つと異なるが、変数や区間の意味と操作は一致している。
- 「出力したい値 min_value は、常にこの中に含まれている」という区間設定。
  - ただし、左開区間(-1, len(nums) - 1]で管理
  - 初期値の-1をleft_exclusive, len(nums) - 1をright_inclusiveとする
- ループを抜ける条件は、left_exclusive + 1 = right_inclusive のとき、このとき、(right_inclusive - 1, right_inclusive]であるため、 returnするのはnums[right_inclusive]になる。
- ループの回し方
  - middle = left + (right - left) // 2 を計算する。(このときleft <= middle < rightが成り立っている)
  - min_valueは[left, middle]か[middle + 1, right]に含まれることが分かる。どちらに含まれているか調べるためには以下の処理を行う
    - nums[0] <= nums[mid] and nums[mid] > nums[-1]かどうか確認。
      - もしそうであれば、middleより右側にmin_valueがあることが確定するので、探索範囲を(middle, right_exclusive]にする
      - そうでなければ、middleかmiddleより左側にmin_valueがあるので、探索範囲を(left_exclusive, middle]にする
        - mid = -1 になるのは、len(nums) == 1のときだが、それはearly returnで対処している。
- 文章が簡潔でとても分かりやすいPRだった。


- https://github.com/Yuto729/leetcode/pull/47 の最初のApproach
- アイデアを記述しておく。
  - こちらも参考にした: https://github.com/Yoshiki-Iwasa/Arai60/pull/35#discussion_r1693974411
- nums[i] < nums[0]となる最小のiを求めればよい。
  - (i = 0 のときは、場合分けして対応。以下の説明では省略する)

- 区間設定は少し工夫されている。
  - 「P(i) の値がまだ確定していないインデックスの集合」を区間とする。ここでP(i)とは P(i) := nums[i] < nums[0]と定義される述語。
    - iとはnumsのインデックス。
    - (P(i)の出力は、述語の定義どおり `True` または `False`)
  - 初期値は left = 0, right = len(nums) とする。

- この区間設定の気持ちは以下のとおり。
- numsの各インデックス0, 1,..., len(nums) - 1に対してP(i)を適用すると
    ```text
    False, False, ... False, True, True, ... True
    ```
    の形になる。
  - 求めたい値は「最初に `True` となるインデックス」
    - なお、すべてFalseのときは0が求めたい値となる

- ループを抜けるときの条件は、未探索のインデックスがないこと。
- また、ループ時の区間の更新方法を工夫することによって、ループを抜けたときにがちょうど求めたい値と対応するインデックスが分かる位置にいるようにする。
  - ループを抜けたときの区間が、False, False, ... False, [True), True, ... Trueになっているということ。

- ループ中の区間の更新方法
  - ループでは未確定なインデックス `mid` を1つ選び、その位置の `P(mid)` を評価する。
    - `P(mid)` が `True` なら、
      - `mid` より右のインデックス `j` についても `P(j) = True` である。したがって、未探索区間は[left, mid)になる。
    - `P(mid)` が `False` なら、
      - `mid` とmidより左のインデックス `j` についても `P(j) = False` である。したがって、未探索区間は[mid + 1, right)になる。


- やりかたはわかったが、区間の設定はまどろっこしく感じる。素直に設定したほうが分かりやすいと感じる。
  - これを使うときは区間を一般的な言葉で説明したいが、いい言葉が思いつかない。
- 良い点は、ある程度型が決まっているので一度覚えれば使いやすいところ。
