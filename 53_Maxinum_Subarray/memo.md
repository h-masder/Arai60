## 問題
https://leetcode.com/problems/maximum-subarray/description/

Given an integer array nums, find the subarray with the largest sum, and return its sum.

Constraints:
1 <= nums.length <= 10^5
-10^4 <= nums[i] <= 10^4


## 進め方
- (step1)問題を見た際に、考えられるアプローチを列挙し、それぞれの計算量を検討する。思いついた方法でコードで表現する。さくっと書けない場合は、他者のコードや生成AIを参考にし、なぜ書けなかったのかを分析して次に活かす。それぞれのコードで3回エラーを出さずに書く。
- 計算量の見積もりについてのコメント: https://github.com/Yuto729/LeetCode_arai60/pull/16#discussion_r2602118324
- (step2)他の人のコードや生成AIを参照し、他のアプローチをコードで表現する。それぞれのコードで3回エラーを出さずに書く。
- (step3)その後、他の人のPRをコードレビューする(PRにコメントを残す)。ここで確認したいのは、この問題の練習会を開き講師としてふるまえるか。
- レビューの仕方: https://google.github.io/eng-practices/review/reviewer/looking-for.html
    - コードレビューは、デザイン、実装、テスト、コーディングスタイルの順に重要。
    - 最終的には、どのPRを見ても他者のコードを素早く理解し、頭の中で実行して妥当性を判断し、必要に応じて修正提案ができる状態を目指す。


## アプローチ

- なんだかうまく解けない。なと思いdiscordをみていたところ、以下のコメントをみつけた。
- https://discord.com/channels/1084280443945353267/1206101582861697046/1207749510797992026
- 納得したのでこんな感じでやってみようと思う（アルゴリズムイントロダクションの動的計画法の章を読んでから、動的計画法を適用できる問題の特徴である部分構造最適性や部分問題重複性を探すことばかりに固執していたので解けていないなと思った。）

- まず、愚直に解いてみる。
- 全部列挙して、どれが最大か調べる
- [2, -3, 1]のとき、全パターンは
  - [2]
  - [-3]
  - [1]
  - [2, -3]
  - [-3, 1]
  - [2, -3, 1]


**実行時間の見積もり**
- numsの長さNとする。numsへのアクセスは、N + (N - 1) + (N - 2) + ...となるため、(N(N + 1) / 2)。制約より、N<=10^5 でだいたい 5* 10^9くらい
- Pythonの実行時間を10^7ステップ/秒とすると、数百秒くらい。

- (code1)
```py
class Solution:
    def maxSubArray(self, nums:List[int]) -> int:
        best = -math.inf
        for i in range(len(nums)):
            candidate = 0
            for j in range(i, len(nums)):
                candidate += nums[j]
                best = max(best, candidate)
        return best
```
- や 

- (code2)
```py
class Solution:
    def maxSubArray(self, nums:List[int]) -> int:
        best = -math.inf
        for i in range(len(nums)):
            candidate = 0
            for j in range(i, -1, -1):
                candidate += nums[j]
                best = max(best, candidate)
        return best
```
- など。


- メモリアクセスを減らしていく。
- (code2) を紙に書いて分かったことは、nums[i] にいるとき、
  - その時点までの最大部分和 A
  - nums[i] を末尾とする最大部分和 B
- が分かればよい、ということ。

- 例えば nums = [2, -3, 1] のとき、
- A: 2,  2,  2
- B: 2, -1,  1

- A は順次更新すればよいとして、B をどう求めるかを考える。
- nums[i] を末尾とする最大部分和 B は、
  「現在までの累積和 prefix_sum」を
  「過去で最小だった累積和 min_prefix_sum」で減算することで求められる。
- prefix_sum が過去最小を更新した場合は、それをmin_prefix_sumとして更新する。

**実行時間の見積もり**
- - numsの長さNとする。制約より、N<=10^5
- numsの各要素に対して、1回のメモリアクセス。各メモリアクセスごとに行う処理は足し算や最大値の計算であり、それを最大でも数十ステップ程度とみなすとそうステップするは10^6程度。
- Pythonの実行時間を10^7ステップ/秒とすると、数百ミリ秒~数秒くらい。

```py
class Solution:
    def maxSubArray(self, nums:List[int]) -> int:
        best = -math.inf
        prefix_sum = 0
        min_prefix_sum = 0
        for i in range(len(nums)):
            prefix_sum += nums[i]
            best = max(best, prefix_sum - min_prefix_sum)
            min_prefix_sum = min(prefix_sum, min_prefix_sum)
        return best
```


- 他の方法として、Kadane's Algorithmがある。
- https://github.com/Manato110/LeetCode-arai60/pull/33
- https://github.com/sakupan102/arai60-practice/pull/33#discussion_r1609314158

- アイデアはシンプルで、nums[i] を末尾とする最大部分和 B は、prefix_sum - min_prefix_sumは別の方法で書ける。それは、
  - 「現在の nums[i] から新しく部分配列を開始する」
  - 「直前までの最大部分和に nums[i] を追加する」
  のどちらかである。

- https://github.com/sakupan102/arai60-practice/pull/33#discussion_r1611415355 では式変形がされている。

```py
class Solution:
    def maxSubArray(self, nums: List[int]) -> int:
        best = -math.inf
        max_including_current_value = 0
        for i in range(len(nums)):
            max_including_current_value = max(nums[i], max_including_current_value + nums[i])
            best = max(best, max_including_current_value)
        return best
```


- 他には分割統治法による解法もある。これまでの方法とは少し遠い。
- https://github.com/Manato110/LeetCode-arai60/pull/33
- https://github.com/mamo3gr/arai60/pull/30

- 原理はわかった。
 - numsの最大部分配列和は、numsを半分に分割したときの左側に入っているか、右側に入っているか、または、両方をまたいでいるか。3つの値を計算して、そのうちの最大値を返せばよい。これを再帰的に行う。

- どういう状況だとこれを選ぶことになるのだろう。
  - まずわかりにくい(クイックソートでやるようなきれいな分割ではないため)。
  - 計算量はO(NlogN)なので、上の改良パターンのほうが計算量は小さい。
  
- こんな方法でも解けますね、くらいにしてとりあえず次に進むことにする。
