# 問題文
- https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/
- You are given an integer array prices where prices[i] is the price of a given stock on the ith day.
- On each day, you may decide to buy and/or sell the stock. You can only hold at most one share of the stock at any time. However, you can sell and buy the stock multiple times on the same day, ensuring you never hold more than one share of the stock.
- Find and return the maximum profit you can achieve.

- Example 1:
- Input: prices = [7,1,5,3,6,4]
- Output: 7
- Explanation: Buy on day 2 (price = 1) and sell on day 3 (price = 5), profit = 5-1 = 4.
- Then buy on day 4 (price = 3) and sell on day 5 (price = 6), profit = 6-3 = 3.
- Total profit is 4 + 3 = 7.

- Example 2:
- Input: prices = [1,2,3,4,5]
- Output: 4
- Explanation: Buy on day 1 (price = 1) and sell on day 5 (price = 5), profit = 5-1 = 4.
- Total profit is 4.

- Example 3:
- Input: prices = [7,6,4,3,1]
- Output: 0
- Explanation: There is no way to make a positive profit, so we never buy the stock to achieve the maximum profit of 0.
 

- Constraints:
- 1 <= prices.length <= 3 * 10^4
- 0 <= prices[i] <= 10^4


# アプローチ
- 毎日株を買う。
- 前日買った株が今日あがっていたら売却。そうでなければ一生握りつぶす。(握りつぶしたものは忘れる。)
- これをすれば、利益はthe maximum profitになる。


- **実行時間の見積もり**
- prices の各要素へ高々1回アクセスするため、アクセス回数は高々 3 * 10^4 回程度。
- 各処理は比較・加算・減算などの軽い処理のみである。
- したがって、全体でも概算で 10^5 ステップ程度で実行できる。
- Pythonの実行速度を10^7ステップ/秒とすると、10msくらいでプログラムの実行が完了する。

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        buying_price = float('inf')
        for price in prices:
            if buying_price < price:
                total_profit += price - buying_price
            buying_price = price
        return total_profit
```


# 他の人のコードを見る
- https://github.com/hiro111208/leetcode/pull/26
- 各整数を折れ線グラフの点と考え、右上がりになるものを合計に加えていく
```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        total_profit = 0
        for i in range(1, len(prices)):
            if prices[i - 1] < prices[i]:
                total_profit += prices[i] - prices[i - 1]
        return total_profit
```

- https://github.com/attractal/leetcode/pull/27
- 何も持っていない状態と株を持っている状態の2つを管理
- 何も持っていない状態になる：
    - 漸化式：  $max(何も持たない,  株を持っている状態から売る)$
- 持っている状態になる：
    - 漸化式： $max(持っていて売らない, 持っていなくて買う)$

```py
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        before_buy = 0          # 何も持ってない状態
        holding = float('-inf') # 株を持ってる状態

        for price in prices:
            new_before_buy = max(before_buy, holding + price)  # 何もしない or 売る
            new_holding = max(holding, before_buy - price)     # 何もしない or 買う

            before_buy = new_before_buy
            holding = new_holding

        return before_buy
```
- 実際に数値を更新しながら追ってみたが、理解できなかった。後日再度チャレンジ。
- before_buyやholdingが何を保持しているのか。



- https://github.com/Yoshiki-Iwasa/Arai60/pull/53/changes#r1730194725
- > もし自分が面接担当で、面接の場でこのコードを書いてもらったら、「では、この利益を実現するための最小売買回数を求められますか？」という質問をしそうだなと思いました。

- Input: prices = [7,1,5,3,6,4]
- Output: 4
- 1で買い、5で売る。3で買い、6で売る。

- Input: prices = [1,2,3,4,5]
- Output: 2
- 1で買い、5で売る。

- Input: prices = [7,6,4,3,1]
- Output: 0
- 買わない

- 最初のコードをから直そうと思ったが、毎日株を買う戦略は使えないので、新しく考えることにした
 - 本来のフォローアップ問題なら、前のコードを土台に修正していくと思う。


- アプローチ
  - 大まかな方針は、最初のコードと同じ。「安いときに買って、高く売る」
  - ただ、株を持っているときに上がり続けているなら持ち続け、持っていないときに下がっているなら、買わないまま待つ。
    - 現実的な取引ではありえないが、次の日の株の価格が分かるとして、コードを書いてみる。


```py
from typing import List
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        if len(prices) <= 1:
            return 0

        total_profit = 0
        buying_price = 0
        holding = False
        num_transactions = 0
        for i in range(len(prices) - 1):
            if prices[i] < prices[i + 1]:
                if holding:
                    continue
                else:
                    buying_price = prices[i]
                    holding = True
                    num_transactions += 1
                    continue
            elif prices[i] > prices[i + 1]:
                if holding:
                    total_profit += prices[i] - buying_price
                    holding = False
                    num_transactions += 1
        
        # 最終日に持っている株は売る
        if holding:
            total_profit += prices[-1] - buying_price
            holding = False
            num_transactions += 1
        
        return total_profit, num_transactions

        
def main():
    solution = Solution()

    prices = [7, 1, 5, 3, 6, 4]
    print(prices, "->", solution.maxProfit(prices))

    prices = [1, 2, 3, 4, 5]
    print(prices, "->", solution.maxProfit(prices))

    prices = [7, 6, 4, 3, 1]
    print(prices, "->", solution.maxProfit(prices))


if __name__ == "__main__":
    main()
```

- output
```text
[7, 1, 5, 3, 6, 4] -> (7, 4)
[1, 2, 3, 4, 5] -> (4, 2)
[7, 6, 4, 3, 1] -> (0, 0)
```
