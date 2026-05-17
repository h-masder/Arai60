## 問題
https://leetcode.com/problems/unique-paths/description/

There is a robot on an m x n grid. The robot is initially located at the top-left corner (i.e., grid[0][0]). The robot tries to move to the bottom-right corner (i.e., grid[m - 1][n - 1]). The robot can only move either down or right at any point in time.

Given the two integers m and n, return the number of possible unique paths that the robot can take to reach the bottom-right corner.

The test cases are generated so that the answer will be less than or equal to 2 * 10~9.

Constraints:

1 <= m, n <= 100



## 進め方
- (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
- 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
- (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
- (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
- レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
    - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
    - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。


## アプローチ

- 紙に書いて調べたところ、以下のような法則がありそうだとわかった

|   | 1 | 2 | 3  | 4  |
|---|---|---|----|----|
| 1 | 1 | 1 | 1  | 1  |
| 2 | 1 | 2 | 3  | 4  |
| 3 | 1 | 3 | 6  | 10 |
| 4 | 1 | 4 | 10 | 20 |

これをコードにする。

```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        num_paths = [[0] * n for _ in range(m)]
        for row in range(m):
            for col in range(n):
                if row == 0 or col == 0:
                    num_paths[row][col] = 1
                    continue
                num_paths[row][col] = num_paths[row - 1][col] + num_paths[row][col - 1]
        return num_paths[m - 1][n - 1]
```
- num_pathsは0で初期化したが1で良かった。

```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        num_paths = [[1] * n for _ in range(m)]
        for row in range(1, m):
            for col in range(1, n):
                num_paths[row][col] = num_paths[row - 1][col] + num_paths[row][col - 1]
        return num_paths[m - 1][n - 1]
```

- ただ、修正前のほうが意図は伝わるかもしれない。


**実行時間の見積もり**
- 1 <= m, n <= 100
- m × n のリストへのアクセスが発生する。各リストアクセスでは数ステップと仮定すると、10^4 から 10^5 ステップくらい
- Pythonの実行時間を10^7ステップ/秒とすると、数ミリ~数十ミリ秒くらい

**他の選択肢を考える**
- すべての経路を列挙し、その個数を返す方法
- 利点: 経路情報そのものを保持しているため、「実際にどのような経路を通ったか」を後から利用したくなった場合に拡張しやすい。
- 欠点: 経路情報をすべて保持するので、メモリ使用量が大きくなる。
  - 問題文には The test cases are generated so that the answer will be less than or equal to 2 * 10^9. という制約がある。
  - つまり、最悪の場合は 2 * 10^9 個近い経路を保持する可能性があり、さらに各経路の長さは最大 (m - 1) + (n - 1) 。


```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        paths = []
        partial_paths = [[(0, 0)]]
        while partial_paths:
            partial_path = partial_paths.pop()
            # current_posison
            row, col = partial_path[-1]
            if row == m - 1 and col == n - 1:
                paths.append(partial_path)
                continue
            if row < m - 1:
                partial_paths.append(partial_path + [(row + 1, col)])
            if col < n - 1:
                partial_paths.append(partial_path + [(row, col + 1)])
        return len(paths)
```




# 他の方の解答を見てみる。

1) 一つ目の方法とアプローチは同じ。ただ、メモリ消費量を減らす取り組みをしている。
  - https://github.com/hiro111208/leetcode/pull/30

|   | 1 | 2 | 3  | 4  |
|---|---|---|----|----|
| 1 | 1 | 1 | 1  | 1  |
| 2 | 1 | 2 | 3  | 4  |
| 3 | 1 | 3 | 6  | 10 |
| 4 | 1 | 4 | 10 | 20 |

- のように表にせずとも
- [1, 1, 1, 1] -> [1, 2, 3, 4] -> [1, 3, 6, 10] -> [1, 4, 10, 20] -> ...と一次元配列で更新すればよい。


```py
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        path_counts = [1] * n
        for _ in range(m - 1):
            for j in range(1, n):
                path_counts[j] += path_counts[j - 1]
        return path_counts[n - 1]
```
- だいぶ省略したので、わかりにくいかもしれない。
- 表を作る方法に比べてこれで空間計算量が小さくなった(O(mn)からO(n)になった)。
- はじめに、以下のチェックをいれると、O(min(m, n))になる。
```py
if m < n:
    m, n = n, m
```

2) Combination
  - https://github.com/Manato110/LeetCode-arai60/pull/34
  - > まんま高校数学でやったCombinationの問題である
  - ちょっと考えて、どこで下に行くかと、どこで右に行くのかを決めるCombinationだとわかった。

```py
import math
class Solution:
    def uniquePaths(self, m: int, n:int) -> int:
        return math.comb(m + n - 2, m - 1)
```

3) メモ化再帰
  - https://github.com/kitano-kazuki/leetcode/blob/62-unique-paths/memo.md#code2-2-recursion--cache
  - 上の表のような計算を右下から再帰的に行うイメージ。

```py
import functools
class Solution:
    def uniquePaths(self, m: int, n: int) -> int:
        @functools.cache
        def unique_path_helper(m, n):
            if m == 1 or n == 1:
                return 1
            return unique_path_helper(m - 1, n) + unique_path_helper(m, n - 1)
        return unique_path_helper(m, n)
```
- 計算量はO(mn)
  - もし、メモ化再帰を使わないと、2*((m + n -2)C(m - 1)) - 1 = O((m + n -2)C(m - 1))
  - 自分では計算量を正確に見積もることができなかった。
  - かなりラフに O(2^(m+n)) と考えていた。
    - 関数呼び出しの再帰木をイメージしていた。
    - 深さは最大でおよそ m + n 程度になり、各ノードで2方向に分岐するため、指数的に増えると考えた。
    - ただし実際には、m か n が 1 になった時点で再帰が終了するため、完全な二分木にはならず、単純な 2^(m+n) ほどは増えない。
  - 以下をみてわかった
    - https://github.com/olsen-blue/Arai60/pull/33#discussion_r1966816399
- @functools.cacheとかlru_cacheとかちゃんとわかっていないので、後で調べる。



- メモ
- https://github.com/fuga-98/arai60/pull/33#discussion_r2040681343
- この辺りに違和感がないことをあたらめて確認。
```py
l = [[0 for _ in range(10)] for _ in range(10)]
print(id(l[0]))
print(id(l[1]))
# 140138653651776
# 140138653651840
l2 = [[0]* 10] * 10
print(id(l2[0]))
print(id(l2[1]))
# 140138653652672
# 140138653652672
```



  
