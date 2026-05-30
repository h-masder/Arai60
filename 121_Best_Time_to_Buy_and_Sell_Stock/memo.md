# 問題文
- リンク: https://leetcode.com/problems/best-time-to-buy-and-sell-stock/description/

- You are given an array prices where prices[i] is the price of a given stock on the ith day.
- You want to maximize your profit by choosing a single day to buy one stock and choosing a different day in the future to sell that stock.
- Return the maximum profit you can achieve from this transaction. If you cannot achieve any profit, return 0.

- Example 1:
- Input: prices = [7,1,5,3,6,4]
- Output: 5
- Explanation: Buy on day 2 (price = 1) and sell on day 5 (price = 6), profit = 6-1 = 5.
- Note that buying on day 2 and selling on day 1 is not allowed because you must buy before you sell.

- Example 2:
- Input: prices = [7,6,4,3,1]
- Output: 0
- Explanation: In this case, no transactions are done and the max profit = 0.

- Constraints:
- 1 <= prices.length <= 10^5
- 0 <= prices[i] <= 10^4


# アプローチ
- 前にといた最大部分和の問題(https://leetcode.com/problems/maximum-subarray/description/)に近いと考えた。
- i日目とi + 1日目の差を計算し、その最大部分和を求めればよいことに気づいた。
  - 差の計算方法の例: prices = [7,1,5,3,6,4]の差は、7-1=6, 1-5=-4,...と計算していき最終的に[-6, 4, -2, 3, -2]となる
  - 最大部分和を求めるために、累積和を使う。
    -  refix_sum を「現在位置までの累積和」とする。
    - minimum_prefix_sum を「これまでに現れた累積和の最小値」とする。
    - 現在位置での最大利益は、prefix_sum - min_prefix_sumで求められる。
    - これを全ての位置で試し、最大値を答えとする。

**実行時間の見積もり**
- i 日目と i + 1 日目の価格差の計算に prices.length 回（高々 10^5 回）のメモリアクセスを行う。
- 累積和を使った最大 profit の計算にも prices.length 回（高々 10^5 回）のメモリアクセスを行う。
- 各要素に対して行う処理は、比較・足し算・引き算程度の定数時間処理のみである。
- したがって、全体の計算量は O(prices.length) となる。
- 最大入力サイズでも、実行ステップ数はおよそ 10^6 程度と見積もられる。
- Python の実行速度を 10^7 ステップ/秒とすると、実行時間はおよそ 100ms 程度になる。

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        price_differences = [0] * (len(prices) - 1)
        for i in range (0, len(prices) - 1):
            price_differences[i] = prices[i + 1] - prices[i]
        
        max_profit = 0
        min_prefix_sum = 0
        prefix_sum = 0
        for price_difference in price_differences:
            prefix_sum += price_difference
            profit = prefix_sum - min_prefix_sum
            if max_profit < profit:
                max_profit = profit
            min_prefix_sum = min(min_prefix_sum, prefix_sum)
        return max_profit
```

- 
# 他の人のコードを見る。
- https://github.com/Manato110/LeetCode-arai60/pull/38 の書いたコード2
- pricesを操作しながら、最小の価格(min_price)を保持し、prices[i] - min_priceが最も大きいものを探す。
- 言われればすごく簡単。こういうのがまずぱっとかけるといいと思う。

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        max_profit = 0
        min_price = prices[0]
        for price in prices:
            max_profit = max(max_profit, price - min_price)
            min_price = min(min_price, price)
        return max_profit
```


- 皆さん大体この解きかたで解いている。とても直感的でわかりやすい。
- 他には特に気になることはないが、いろいろ考えている方もいる。後で確認できるように載せておく
  - https://github.com/Yuto729/leetcode/pull/42
  - https://github.com/arahi10/coding-practice/pull/4
