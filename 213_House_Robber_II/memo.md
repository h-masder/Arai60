# 問題文
You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are arranged in a circle. That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and it will automatically contact the police if two adjacent houses were broken into on the same night.

Given an integer array nums representing the amount of money of each house, return the maximum amount of money you can rob tonight without alerting the police.

# 入力例
- Example 1:
- Input: nums = [2,3,2]
- Output: 3
- Explanation: You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.

- Example 2:
- Input: nums = [1,2,3,1]
- Output: 4
- Explanation: Rob house 1 (money = 1) and then rob house 3 (money = 3).
- Total amount you can rob = 1 + 3 = 4.

- Example 3:
- Input: nums = [1,2,3]
- Output: 3


- Constraints:
- 1 <= nums.length <= 100
- 0 <= nums[i] <= 1000


# アプローチ
- 前問とアイデアは同じ。目の前の家のお金を盗むか、もしくは盗まないかの二択。
- 前問と違う部分は盗む範囲。もし、nums[0]を盗んだ場合、nums[-1]から盗むことはできない。
- nums[0]からnums[-2]までの探索と、nums[1]からnums[-1]までの探索を行う。似た探索をやっているので冗長かもしれないが、ひとまずこれで書いてみる。

**実行時間の見積もり**
- nums[0]からnums[-2]までの探索と、nums[1]からnums[-1]までの探索を考えると、numsへのメモリアクセスは、高々200回程度
- 各メモリアクセスは数十ステップの処理とすると、10^3~10^4ステップの処理で終わる
- Pythonの実行速度を10^7ステップ/秒とすると1ms以下で終わる。

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        max_money_without_head = [0] * (len(nums) + 1) # max_money_without_head[i] == rob(nums[1:i])
        max_money_without_tail = [0] * (len(nums) + 1) # max_money_without_tail[i] == rob(nums[:i - 1])
        for i in range(2, len(max_money_without_head)):
            max_money_without_head[i] = max(max_money_without_head[i - 1], max_money_without_head[i - 2] + nums[i - 1])
            max_money_without_tail[i] = max(max_money_without_tail[i - 1], max_money_without_tail[i - 2] + nums[i - 2])
        return max(max_money_without_head[-1], max_money_without_tail[-1])
```
- submitでエラーを出した。numsの長さが1のときを考慮できていなかった。
- 再帰も書いてみた。
```py
from functools import cache
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        @cache
        def rob_from(house_index: int, end_index: int) -> int:
            if house_index >= end_index:
                return 0
            max_money_without_current_house = rob_from(house_index + 1, end_index)
            max_money_with_current_house = nums[house_index] + rob_from(house_index + 2, end_index)
            return max(max_money_without_current_house, max_money_with_current_house)
        return max(rob_from(0, len(nums) - 1), rob_from(1, len(nums)))
```



# 他の人のコードを見る。
- おおかた同じような解きかた。
- しいて言えば、盗めるお金の合計をリストで管理せずに数値で管理する方法もある。
- https://github.com/naoto-iwase/leetcode/pull/41

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        if not nums:
            return 0
        if len(nums) == 1:
            return nums[0]
        
        def rob_section(start_index: int, end_index: int) -> int:
            money_with_last_house = 0
            money_without_last_house = 0
            for i in range(start_index, end_index + 1):
                money_with_last_house, money_without_last_house = (
                    nums[i] + money_without_last_house,
                    max(money_with_last_house, money_without_last_house)
                )
            return max(money_with_last_house, money_without_last_house)
        return max(rob_section(0, len(nums) - 2), rob_section(1, len(nums) - 1))
```
