## 問題
https://www.lintcode.com/problem/514/

There is a fence with n posts, each post can be painted with one of the k colors.
You have to paint all the posts such that no more than two adjacent fence posts have the same color.
Return the total number of ways you can paint the fence.

## 進め方
- 最近いろいろなやり方を模索しています。かなり迷走していますが、ひとまずこれでやります。
  - (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
    - 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
  - (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
  - (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
    - レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
      - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
      - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。

## アプローチ

- 簡単な例を書きながら法則を見つけた。
  - (n, k) = (1, 1), (1, 2), (1, 3), (2, 1), (2, 2), (2, 3), (3, 1), (3, 2), (3, 3) で試した。
  - n = 1 のとき、returnするのは k
  - n = 2 のとき、returnするのは k * k
  - n = 3 のとき、
    - n >= 3, k = 1 なら、returnするのは 0
    - それ以外は、returnするのは last_two_same_color_count_3 + last_two_different_color_count_3
      - last_two_same_color_count_i とは n = i のときの全パターンのうち、最後の2色が同色のもの
      - last_two_different_color_count_i とは n = i のときの全パターンのうち、最後の2色が異色のもの
      - last_two_same_color_count_i = last_two_different_color_count_(i - 1)が成り立つ。 
      - last_two_different_color_count_i = (k - 1) * (last_two_same_color_count_(i - 1) + last_two_different_color_count_(i - 1))が成り立つ。
      - (last_two_same_color_count_2 = k が成り立つ)
      - (last_two_different_color_count_2 = k * (k - 1) が成り立つ。)


**実行時間の見積もり**
- 最大 n のループが定数ステップで回る
- 制約は明記されていない
- Pythonの実行ステップを10^7ステップ/秒くらいとすると、n = 10^7でも数秒くらい
```py
class Solution:
    def numWays(self, n: int, k: int) -> int:
        if n == 1:
            return k
        if n == 2:
            return k * k
        if n >= 3 and k == 1:
            return 0

        last_two_same_color_count = k
        last_two_different_color_count = k * (k - 1)
        num_ways = last_two_same_color_count + last_two_different_color_count
        for i in range(3, n + 1):
            previous_same = last_two_same_color_count
            previous_diff = last_two_different_color_count
            last_two_same_color_count = previous_diff
            last_two_different_color_count = (k - 1) * (previous_same + previous_diff)
            num_ways = last_two_same_color_count + last_two_different_color_count
        return num_ways
```

- 少し整理すると、

```py
class Solution:
    def numWays(self, n: int, k: int) -> int:
        if n == 1:
            return k
        if n == 2:
            return k * k
        if n >= 3 and k == 1:
            return 0

        last_two_same_color_count = k
        last_two_different_color_count = k * (k - 1)
        for _ in range(3, n + 1):
            last_two_same_color_count, last_two_different_color_count = (
                last_two_different_color_count, 
                (k - 1) * (last_two_same_color_count + last_two_different_color_count)
            )

        return last_two_same_color_count + last_two_different_color_count
```
- これだけでつたわるだろうか.


- 他の解きかたは、システマティックに考えると、トップダウンアプローチがある。他の人の解答をみた。
- https://github.com/shining-ai/leetcode/pull/30/changes#diff-a7a4b655731fbb220206ff9305969b66ac8cf7fd64bdcd12cbe6837749eac7bfR1-R9 のメモ化再帰
- 以下、コードの抜粋

```py
class Solution:
    def numWays(self, n: int, k: int) -> int:
        num_way_memo = {}
        num_way_memo[1] = k
        num_way_memo[2] = k**2

        def count_num_way(n):
            if n in num_way_memo:
                return num_way_memo[n]
            same_as_previous = (k - 1) * count_num_way(n - 2)
            different_from_previous = (k - 1) * count_num_way(n - 1)
            num_way_memo[n] = same_as_previous + different_from_previous
            return num_way_memo[n]

        return count_num_way(n)
```
- 考え方
- post が n 本あるときの塗り方の数を A(n) とする。
- A(n) は、n 本目を 直前と異なる色にする場合 と 同じ色にする場合 に分けて考えられる。
- n 本目を n-1 本目と異なる色にする場合
  - n-1 本までの塗り方は A(n-1) 通り
  - n 本目は直前と違う色を選ぶので k-1 通り
  - 合計 A(n-1) × (k-1) 通り
- n 本目を n-1 本目と同じ色にする場合
  - 3 連続を避けるため、n-1 本目と n-2 本目は異なる必要がある
  - つまり、この場合は「n-2 本までの塗り方」から考える
  - n-2 本までの塗り方は A(n-2) 通り
  - n-1 本目は n-2 本目と異なる色を選ぶので k-1 通り
  - n 本目は n-1 と同じ色（1通り）
  - → 合計 A(n-2) × (k-1) 通り
- したがって A(n) = (k-1) × (A(n-1) + A(n-2))

- 感想
  - nが大きいと、再帰の上限に引っ掛かる。
  - n >= 3, k = 1 のときがケアされているか、を考えさせてしまいそうなので、それについては、丁寧に書いたほうが良いかもしれない。
  - だとすると、ボトムアップのほうが最初の選択肢になりそう。

- Dynamic Programmingは、いろいろな解きかたがありそうなので、全部を練習するというより自分で法則を見つけて解くことと他の人のコードをレビューすることに重きを置いたほうがよさそう。

## 他の人のコードを読み、気になることがあればレビューする。

- https://github.com/hiro111208/leetcode/pull/24
- https://github.com/tom4649/Coding/pull/57/
- https://github.com/Manato110/LeetCode-arai60/pull/31/changes#r3186811879
- https://github.com/kitano-kazuki/leetcode/pull/30/


#### 余談
- 自分がコーディング試験の面接官なら、Dynamic Programmingの問題を選びたくなる。
  - こういったアルゴリズムは、仕事で書きそう
  - 過去問と違う形で出題できる(大体似たような解きかたにはなりそうだが)
  - 解きかたを見つけコードに起こしたところで、法則を知らない人にとってはなんだかよくわからない解答になる可能性がある。将来のこのコードを見る人が分かりやすいと思える情報を残せるかが見れる。
