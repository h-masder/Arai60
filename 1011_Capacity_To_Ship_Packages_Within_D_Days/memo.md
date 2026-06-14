# 問題文
- https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/

- A conveyor belt has packages that must be shipped from one port to another within days days.
- The ith package on the conveyor belt has a weight of weights[i]. Each day, we load the ship with packages on the conveyor belt (in the order given by weights). We may not load more weight than the maximum weight capacity of the ship.
- Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within days days.


- Example 1:
- Input: weights = [1,2,3,4,5,6,7,8,9,10], days = 5
- Output: 15
- Explanation: A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
- 1st day: 1, 2, 3, 4, 5
- 2nd day: 6, 7
- 3rd day: 8
- 4th day: 9
- 5th day: 10

- Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.

- Constraints:
- 1 <= days <= weights.length <= 5 * 10^4
- 1 <= weights[i] <= 500

# アプローチ
- 求めたいのは、すべての荷物を days 日以内に運べる最小の船のcapacityである。
- 取りうる capacityの範囲 1 <= capacity <= (weights[i]の最大値) * (weightsの長さ)に対して、
- 言い換えると、
  - capacity - 1 では運べない
  - capacityでは運べる
- となるcapacityを探したい。(これを思いつくのに少し時間がかかった。)

- 容量を小さい方から順に試していくこともできるが、二分探索で行うと効率がよいので、そうする。
- 二分探索
   - **初期設定**
   - [0, 1, 2, ..., (weights[i]の最大値) * (weightsの長さ)]という区間を設定する。この区間で運べないcapacityと運べるcapacityの境界を管理する。
     - 0は絶対に運べない。これをunshippable_capacityとする。unshippable_capacityとこれより左は運べない。
     - (weights[i]の最大値) * (weightsの長さ)は1日あれば運べる。これをshippable_capacityとする。unshippable_capacityとこれより右は運べる。
   - **探索**
   - capacity_to_try = (unshippable_capacity + shippable_capacity) // 2 に対して、引数として与えられたdays以内に運べるかチェックする。方針は以下の通り
     - 詰め込みたい荷物の単体の重さがcapacityをこえていたら、運べない（return False）
     - 詰め込みたい荷物の合計が capacityをこえたら、その荷物は次の日に送る。これを繰り返した結果、daysをこえるなら運べない（return False）。daysを超えないなら運べる（return True）
     - チェックは前から順に入れていって、days以内に送れるか調べる。
  - もし運べなかったら、unshippable_capacity = capacity_to_try
  - 運べたら、shippable_capacity = capacity_to_try
  - unshippable_capacity + 1 = shippable_capacityになったら探索を終了する。unshippable_capacity + 1かshippable_capacityを返せばよい

**実行時間の見積もり**
- [0, 1, 2, ..., (weights[i]の最大値) * (weightsの長さ)]の二分探索にかかるメモリアクセスは、
  - (weights[i]の最大値) * (weightsの長さ) = 5 *10^2 * 5 * 10^4 = 2.5 = 10^7 で、25回くらい
  - 各メモリアクセスでは、`capacity_to_tryで運べるかチェックする`を行う。このとき、weightsの長さだけメモリアクセスするので、5 * 10^4くらい。
  - 25 * (5 * 10^4) で1.25 + 10^5。他の処理とあわても10^6ステップくらいかかる。
  - Pythonの実行時間が10^7ステップ/秒くらいとすると100msくらい



```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def check_shipping_within_days(capacity):
            day_count = 1
            loaded = 0

            for weight in weights:
                if capacity < weight:
                    return False

                if capacity < loaded + weight:
                    loaded = 0 # 出荷
                    day_count += 1
                    if days < day_count:
                        return False

                loaded += weight

            return True
        
        MAX_WEIGHT = 500
        unshippable_capacity = 0
        shippable_capacity = MAX_WEIGHT * len(weights)

        while unshippable_capacity + 1 < shippable_capacity:
            capacity_to_try = (unshippable_capacity + shippable_capacity) // 2
            if check_shipping_within_days(capacity_to_try):
                shippable_capacity = capacity_to_try
            else:
                unshippable_capacity = capacity_to_try               

        return shippable_capacity
```

# 他の人のコードを見る
- 1) 自分のやり方と似たような解法で、区間の設定方法が違うもの。
- https://github.com/Manato110/LeetCode-arai60/pull/45 のステップ0
  - 設定方法
    - 左端: left_capacity = max(weights)
    - 右端: right_capacity = sum(weights)
    - コードがシンプルになる。一応max()とsum()は2*weightsだけメモリアクセスが増えるが、大差ない。（探索区間も短くなっているので、check_shipping_within_daysの呼び出し回数が数回減るかもしれないので、そういう意味でも実行時間は大差ない）

- 自分で書いたコードを修正してみた。
```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def check_shipping_within_days(capacity):
            day_count = 1
            loaded = 0

            for weight in weights:
                if capacity < loaded + weight:
                    loaded = 0 # 出荷
                    day_count += 1
                    if days < day_count:
                        return False

                loaded += weight

            return True
        

        unshippable_capacity = max(weights) - 1
        shippable_capacity = sum(weights)

        # 以下省略
```

- https://github.com/olsen-blue/Arai60/pull/44 の解法1
  - 解法1: こちらも自分のやり方と似たような解法。


- 2) bisect_leftを使う方法。
  - https://github.com/tom4649/Coding/pull/42
  - https://github.com/olsen-blue/Arai60/pull/44 の解法2
    - なるほど。こういう使い方もできるのか。
```py
class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        def check_shipping_within_days(capacity):
            day_count = 1
            loaded = 0

            for weight in weights:
                if capacity < loaded + weight:
                    loaded = 0 # 出荷
                    day_count += 1
                    if days < day_count:
                        return False

                loaded += weight

            return True

        return bisect.bisect_left(range(sum(weights) + 1), True, lo=max(weights), key=check_shipping_within_days) 
```

- 3) `check_shipping_within_days`のような運べるかのチェックにbisect_leftを使用。
- https://github.com/kitano-kazuki/leetcode/pull/44
  - 参考程度かな。割とコードを追うのが大変。


- メモ
- 他の人の二分探索のやり方をもっとわかるようになりたいので、その観点で見た。
- 大体は以下のような書き方。（https://github.com/Manato110/LeetCode-arai60/pull/45 のコードを抜粋）

```py
        min_capacity = max(weights)
        max_capacity = sum(weights)
        
        while min_capacity < max_capacity:
            middle_capacity = (min_capacity + max_capacity) // 2
            
            if self._is_shippable(middle_capacity, weights, days):
                max_capacity = middle_capacity
            else:
                min_capacity = middle_capacity + 1

        return min_capacity
```

- 探索範囲は `max(weights)` から `sum(weights)` までである。
  - `max(weights)` 未満では最も重い荷物を積めないため運べない。
  - `sum(weights)` なら全ての荷物を1日で運べるため運べる。

  - 閉区間探索:[ 未探索 ... 未探索 | 運べる ]
  - 半開区間探索: [ 未探索 ... 未探索 )
  - のいずれかで探索する。更新方法やループの抜け方、returnする値はどちらも選んでも同じ。


- https://github.com/olsen-blue/Arai60/pull/44 の解法1
```py
        def find_min_capacity(low: int, high: int) -> int:
            if low == high:
                return low
            middle = (low + high) // 2
            if is_loadable_capacity(middle):
                return find_min_capacity(low, middle)
            else:
                return find_min_capacity(middle + 1, high)
        return find_min_capacity(0, sys.maxsize + 1)
```

- PRでは以下のように書いてある。
  - capacityとして取りうる値の範囲を[left, right)として、middleの位置のチェックによって、middleの位置まで、探索打ち切り区間の先頭 F or T(left-1 or right)が伸びてくる。
  - 初期範囲の値は、[0, len())とする。探索打ち切り区間の先頭(-1, len())は、探索区間の外、つまりまだ何も探索していない状態。
  - 終了条件は、探索区間の消失(打ち切り区間の衝突)のタイミング、つまり left == right のとき

- これに対して思ったことは、
- capacity = 0 では、運べないことは（weightsをみなくても）自明なので、capacityとして取りうる値の範囲としては適切ではない。初期値は、[1, sys.maxsize + 1)のほうが良い。
- 初期値の変更によって区間の更新（縮め方）を変える必要はない。capacityがmiddleのとき
  - 運べるときは、[low, middle]で良いし、
  - 運べないなら、[middle + 1, right]でよい。

- （自分用のメモ：二分探索の区間初期値で2以上かつif low == highという終了条件なら、必ず最後は[left, right)という長さ2の区間を見ることになる。この事実は、ループを抜けるときなどの細部のチェックに必須。）
