# 問題文
- https://leetcode.com/problems/coin-change/description/
- You are given an integer array coins representing coins of different denominations and an integer amount representing a total amount of money.
- Return the fewest number of coins that you need to make up that amount. If that amount of money cannot be made up by any combination of the coins, return -1.
- You may assume that you have an infinite number of each kind of coin.

- Example 1:
- Input: coins = [1,2,5], amount = 11
- Output: 3
- Explanation: 11 = 5 + 5 + 1

- Example 2:
- Input: coins = [2], amount = 3
- Output: -1

- Example 3:
- Input: coins = [1], amount = 0
- Output: 0

- Constraints:
- 1 <= coins.length <= 12
- 1 <= coins[i] <= 231 - 1
- 0 <= amount <= 104

# アプローチ
- 便宜上 amountの貨幣単位は円とする。
- 方針として思いつくのは二つ。
  - 1) 一枚ずつ両替をしていき、枚数が少ないものを探す
  - 2) 1円のときの最小のコイン、2円のときの最小のコイン、... と調べていき、amount円のときの最小のコインを導く

- 1) 一枚ずつ両替をしていき、枚数が少ないものを探す
  - ある残金に対して、各コインを使う場合をそれぞれ試す。
  - 状態として、残金とこれまでに使用したコイン枚数を保持する。
  - コインを1枚使うたびに、残金からそのコインの額面を引き、使用コイン枚数を1増やす。
  - 残金が0になった場合は両替成功なので、そのときの使用コイン枚数で最小値を更新する。
  - すべての組み合わせを試し、その中で最も使用コイン枚数が少ないものを答えとする。
  
  - 実行時間削減のために：
    - 同じ残金を何度も試すため、各残金について「その残金に到達したときの最小の使用コイン枚数」を記録しておく。
    - ある残金に対して、過去に記録した枚数以上のコインを使って到達した場合、その後の探索を行ってもより良い解は得られないため、その探索を打ち切

**実行時間の見積もり**
- 同じ残金を一度も試さなければ、O(len(coins) * amount)、もし全探索になったら、O(len(coins)^amount)
- O(len(coins) * amount)なら100msくらい。
  - 1 <= coins.length <= 12, 0 <= amount <= 10^4なので、1.2 * 10^5くらいのメモリアクセス。各メモリアクセスで重たい処理は走らないので数十ステップくらいとすると、そうステップ数は10^6くらい。Pythonの実行時間を10^7ステップ/秒とすると100msくらい。
- O(len(coins)^amount)は、現実的な時間では終わらない。
- これ以上、正確に見積もる方法が分からない。
- 入力次第で大きく変わる。性能要件が厳しいプリケーションでは採用の見送りも検討。あとは、入力がある程度決まっているなら、それを入れて実測を測って採用するかどうか決めると思う。


```py
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        balance_and_counts = [(amount, 0)]
        min_num_coins = float("inf")
        balance_to_min_num_coins = {}
        while balance_and_counts:
            balance, count = balance_and_counts.pop()
            if balance == 0:
                min_num_coins = min(min_num_coins, count)
                continue

            if balance in balance_to_min_num_coins:
                if balance_to_min_num_coins[balance] <= count:
                    continue
            balance_to_min_num_coins[balance] = count
            
            for coin in coins:
                new_balance = balance - coin
                if new_balance >= 0:
                    balance_and_counts.append((new_balance, count + 1))
                    
        return -1 if min_num_coins == float("inf") else min_num_coins
```

- 8秒くらいかかっていた。

- 2) 0円のときの最小のコイン、1円のときの最小のコイン、2円のときの最小のコイン、... と調べていき、amount円のときの最小のコインを導く
  - X円のときの最小コイン枚数は、X - (各コイン) 円のときの最小コイン枚数に1を足したものの最小値になる。
  - これを amount 円まで繰り返す。

**実行時間の見積もり**
- 0~からamount円に対して、X - (各コイン) 円を計算するので、O(len(coins) * amount)
  - 1 <= coins.length <= 12, 0 <= amount <= 10^4なので、1.2 * 10^5くらいのメモリアクセス。min関数が走るくらいなので、各メモリアクセスにおけるステップ数を数十ステップくらいとすると、総ステップ数は10^7くらい。Pythonの実行時間を10^7ステップ/秒とすると1sくらい。

```py
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        min_num_coins = [float("inf")] * (amount + 1)
        min_num_coins[0] = 0

        for i in range(1, len(min_num_coins)):
            for coin in coins:
                if i - coin >= 0:
                    min_num_coins[i] = min(min_num_coins[i], min_num_coins[i - coin] + 1)
        
        return -1 if min_num_coins[amount] == float("inf") else min_num_coins[amount]
```



# 他の人のコードをみる。

- アプローチ2)と同じアイデア
  - https://github.com/hiro111208/leetcode/pull/33
- アプローチ1)の再帰バージョン
  - https://github.com/Manato110/LeetCode-arai60/pull/41 のステップ1
  - https://github.com/kitano-kazuki/leetcode/tree/322-coin-change
    
- 幅優先探索
  - https://github.com/attractal/leetcode/pull/29
  - https://github.com/attractal/leetcode/pull/29
    - コインの枚数に対して、取りうる金額を見ていく。
      - 例えば、coins = [1, 5, 7], amount = 11なら、
         - コイン一枚のとき：1, 5, 7
         - コイン二枚のとき: 2, 6, 8, 10, 12
         - コイン三枚のとき：3, 7, 9, 11, 13, 15, 19, 17
　　　　　- (計算が間違っているかもしれないが、こんなイメージ)


- 幅優先なら、コインの数に対して、取りうる金額を保持しながら処理すると見やすいかなと思った。
```py
class Solution:
    def coinChange(self, coins, amount):
        if amount == 0:
            return 0

        possible_amounts = [0]
        num_coins = 0
        visited_amounts = {0}
        while possible_amounts:
            next_possible_amounts = []
            for current_amount in possible_amounts:
                for coin in coins:
                    new_amount = current_amount + coin
                    if new_amount == amount:
                        return num_coins + 1
                    
                    if new_amount > amount:
                        continue
                    
                    if new_amount not in visited_amounts:
                        next_possible_amounts.append(new_amount)
                        visited_amounts.add(new_amount)

            possible_amounts = next_possible_amounts
            num_coins += 1
            
        return -1
```



- メモ
- https://github.com/Yuto729/leetcode/pull/45/changes#r3097018219
  - 一行の長さについて
  - > 1 行が長すぎるように感じました。Pythonのプロジェクトでよく用いられている black なら 88 文字、flake8 とかで PEP8 をチェックするなら 79 文字、過去所属していたチームでは 120 文字が最大で、それくらいに揃えた方がコンパクトにまとまって読みやすいように思います。
