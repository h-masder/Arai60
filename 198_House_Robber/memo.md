## アプローチ
- i 番目の家を盗んだ場合、次に盗める候補はi + 2 かi + 3 のどちらかになる。また、nums[0] に該当する家から盗み始めるか、nums[1]に該当する家から盗み始めるかの2択がある。
- 例えば、house0~house5のお金が
```text
nums = [2, 7, 9, 3, 1]
```
のとき以下の盗み方がある。

```text
start
├── house 0 (2)
│   ├── house 2 (9)
│   │   └── house 4 (1)
│   │
│   └── house 3 (3)
│
└── house 1 (7)
    ├── house 3 (3)
    │
    └── house 4 (1)
```
これの最大値がわかればよい。house i の次は house i + 2 もしくは hosue i + 3のどちらかが訪問する候補となる。

- 上記の木構造を深さ優先探索で調べると良さそうと感じた。
- whileバージョンと再帰バージョンで書く。再帰をメモ化すれば計算量は抑えられる。

- whileバージョン

**実行時間の見積もり**
  - 各木のノード i から、i + 2, i + 3 への2つの分岐が発生する。探索の深さはおおよそ n / 2 程度である。
  - したがって、状態数は概ね O(2^(n/2)) 程度。これは時間がかかりすぎる。
  - 例えば nums の長さが100の場合、ノード数は 2^50 ≒ 10^15 となる。
  - Python の実行速度を 10^7 ステップ/秒 とすると、10^15 / 10^7 = 10^8 秒程度かかる計算になる。


```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        index_and_total = [(0, nums[0]), (1, nums[1])]
        max_money = 0
        while index_and_total:
            index, total = index_and_total.pop()
            if index + 2 >= num_houses:
                max_money = max(max_money, total)
                continue
            else:
                index_and_total.append((index + 2, total + nums[index + 2]))
            
            if not(index + 3 >= num_houses):
                index_and_total.append((index + 3, total + nums[index + 3]))
        
        return max_money


```

- メモ化再帰バージョン
- **実行時間の見積もり**
  - 計算結果を保存すれば、各indexに対して再帰関数の処理は一度で済む。
  - 再帰関数内で行う処理は数十ステップ程度なので、全体のステップ数を多めに見積もっても 10^4 程度。
  - Python の実行速度を 10^7 ステップ/秒 とすると、実行時間は 1ms 程度になる。

- （生成AIを使って変数名、関数名を修正した）

```py
from functools import cache
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        @cache
        def rob_from(house_index: int) -> int:
            if house_index + 2 >= num_houses:
                return nums[house_index]

            money_from_next_house = rob_from(house_index + 2)
            money_from_house_after_next = rob_from(house_index + 3) if house_index + 3 < num_houses else 0
            return nums[house_index] + max(money_from_next_house, money_from_house_after_next)
            
        return max(rob_from(0), rob_from(1))
```

メモ化再帰の処理を、while文でも書き直せそうだと思った。

```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        max_money = [0] * num_houses
        house_index = num_houses - 1
        while house_index >= 0:
            max_money_from_next_house = max_money[house_index + 2] if house_index + 2 < num_houses else 0
            max_money_from_house_after_next = max_money[house_index + 3] if house_index + 3 < num_houses else 0
            max_money[house_index] = nums[house_index] + max(max_money_from_next_house, max_money_from_house_after_next)
            house_index -= 1
        
        return max(max_money[0], max_money[1])
```

## 他の人の解答を見る
- $house(n)$まで訪れた時の最大の額$maxAmount(n)$は、$max(house(n) + maxAmount(n-2), maxAmount(n-1))$である
- https://github.com/hiro111208/leetcode/pull/25
- https://github.com/Manato110/LeetCode-arai60/pull/36
- https://github.com/Yoshiki-Iwasa/Arai60/pull/50/files/3046fa9275ad29e7ea77647922aef66f2a607c91#r1717915563
    > 各家の前に、泥棒の手下が一人ずつ立って、前から伝言をもらって、最後のところで求めたい数字を知りたいとします。「伝言」の内容は「ここまで最大いくら取れる、俺の眼の前の家に盗みに入らないとすると最大いくら取れる」の二つだけじゃないですか。
    - 確かにその通り。

- 上記のコードやコメントを見ながら、再帰がもっとシンプルに書けると思ったので書いてみる。

```py
from functools import cache
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        @cache
        def rob_from(house_index: int) -> int:
            if house_index >= num_houses:
                return 0
            
            money_without_current_house = rob_from(house_index + 1)
            money_with_current_house = nums[house_index] + rob_from(house_index + 2)

            return max(money_without_current_house, money_with_current_house)
        
        return rob_from(0)
```

- while: 前から
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        max_money_up_to = [0] * (num_houses)
        max_money_up_to[0] = nums[0]
        max_money_up_to[1] = max(nums[0], nums[1])
        house_index = 2
        while house_index < num_houses:
            money_without_current_house = max_money_up_to[house_index - 1]
            money_with_current_house = nums[house_index] + max_money_up_to[house_index - 2]
            max_money_up_to[house_index] = max(money_without_current_house, money_with_current_house)

            house_index += 1
        
        return max_money_up_to[num_houses - 1]
```
- while: うしろから
```py
class Solution:
    def rob(self, nums: List[int]) -> int:
        num_houses = len(nums)
        if num_houses == 0:
            return 0
        if num_houses == 1:
            return nums[0]
        
        max_money_from = [0] * (num_houses)
        max_money_from[num_houses - 1] = nums[num_houses - 1]
        max_money_from[num_houses - 2] = max(nums[num_houses - 1], nums[num_houses - 2])
        house_index = num_houses - 3
        while house_index >= 0:
            money_without_current_house = max_money_from[house_index + 1]
            money_with_current_house = nums[house_index] + max_money_from[house_index + 2]
            max_money_from[house_index] = max(money_without_current_house, money_with_current_house)

            house_index -= 1
        
        return max_money_from[0]

```
